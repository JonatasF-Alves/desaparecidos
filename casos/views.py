from urllib.parse import quote

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CasoForm
from .models import Caso



class CasoListView(ListView):
    template_name = "casos/lista.html"
    context_object_name = "casos"
    paginate_by = 12

    def get_queryset(self):
        qs = Caso.objects.filter(aprovado=True)
        busca = self.request.GET.get("q")
        if busca:
            qs = qs.filter(Q(nome__icontains=busca) | Q(cidade__icontains=busca))
        return qs


class CasoDetailView(DetailView):
    template_name = "casos/detalhe.html"
    context_object_name = "caso"

    def get_queryset(self):
        return Caso.objects.filter(aprovado=True)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        url = self.request.build_absolute_uri()
        ctx["whatsapp"] = "https://wa.me/?text=" + quote(f"Ajude a encontrar {self.object.nome}: {url}")
        return ctx


class CasoCreateView(LoginRequiredMixin, CreateView):
    form_class = CasoForm
    template_name = "casos/form.html"
    success_url = reverse_lazy("casos:lista")

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["usuario"] = self.request.user
        return kwargs    

    def form_valid(self, form):
        form.instance.dono = self.request.user
        messages.success(self.request, "Cadastro enviado. Ele será publicado depois da análise da equipe.")
        return super().form_valid(form)

class MeusCasosView(LoginRequiredMixin, ListView):
    template_name = "casos/meus_casos.html"
    context_object_name = "casos"

    def get_queryset(self):
        return Caso.objects.filter(dono=self.request.user)