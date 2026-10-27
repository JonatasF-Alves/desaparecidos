from urllib.parse import quote

from django.db import IntegrityError, transaction
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.views.decorators.http import require_POST

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .forms import CasoForm, DenunciaForm
from .models import Caso, Denuncia

LIMITE_DENUNCIAS = 100

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

@login_required
@require_POST
def marcar_encontrado(request, pk):
    caso = get_object_or_404(Caso, pk=pk, dono=request.user)
    caso.status = "encontrado"
    caso.data_encontrado = timezone.localdate()
    caso.save(update_fields=["status", "data_encontrado"])
    messages.success(request, f"{caso.nome} foi marcado(a) como encontrado(a). Que bom!")
    return redirect("casos:meus_casos")

class DenunciarView(LoginRequiredMixin, CreateView):
    form_class = DenunciaForm
    template_name = "casos/denunciar.html"
    success_url = reverse_lazy("casos:lista")

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.caso = get_object_or_404(Caso, pk=kwargs["pk"], aprovado=True)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            if self.caso.dono_id == request.user.id:
                messages.error(request, "Você não pode denunciar o seu próprio cadastro.")
                return redirect("casos:detalhe", pk=self.caso.pk)
            if Denuncia.objects.filter(caso=self.caso, autor=request.user).exists():
                messages.info(request, "Você já denunciou este cadastro.")
                return redirect("casos:detalhe", pk=self.caso.pk)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["caso"] = self.caso
        return ctx

    def form_valid(self, form):
        form.instance.caso = self.caso
        form.instance.autor = self.request.user
        try:
            with transaction.atomic():
                response = super().form_valid(form)
        except IntegrityError:
            messages.info(self.request, "Você já denunciou este cadastro.")
            return redirect("casos:detalhe", pk=self.caso.pk)

        if self.caso.denuncias.count() >= LIMITE_DENUNCIAS:
            Caso.objects.filter(pk=self.caso.pk).update(aprovado=False)
        messages.success(self.request, "Denúncia enviada. Obrigado por ajudar a manter o site confiável.")
        return response