from datetime import timedelta

from django import forms
from django.utils import timezone

from .models import Caso

LIMITE_CASOS_POR_DIA = 2


class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ["nome", "idade", "foto", "cidade", "estado",
                  "data_desaparecimento", "descricao", "contato", "numero_bo"]
        widgets = {"data_desaparecimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario

    def clean(self):
        cleaned_data = super().clean()
        
        if self.usuario is None or self.usuario.is_superuser:
            return cleaned_data    
        desde = timezone.now() - timedelta(hours=24)
        total = Caso.objects.filter(dono=self.usuario, criado_em__gte=desde).count()
        
        if total >= LIMITE_CASOS_POR_DIA:
            raise forms.ValidationError(
                f"Você já cadastrou {LIMITE_CASOS_POR_DIA} casos nas últimas 24 horas. "
                "Tente novamente mais tarde."
            )            
        return cleaned_data

    