from datetime import timedelta
from .turnstile import TurnstileField

from django import forms
from django.utils import timezone

from .models import Caso, Denuncia

LIMITE_CASOS_POR_DIA = 2

TAMANHO_MAX_FOTO = 5 * 1024 * 1024  # 5 MB, em bytes
FORMATOS_FOTO = {"image/jpeg", "image/png", "image/webp"}

class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ["nome", "idade", "foto", "cidade", "estado",
                  "data_desaparecimento", "descricao", "contato", "numero_bo"]
        widgets = {"data_desaparecimento": forms.DateInput(attrs={"type": "date"})}

    def __init__(self, *args, usuario=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.usuario = usuario
        self.fields["cf-turnstile-response"] = TurnstileField()

    def clean_foto(self):
        foto = self.cleaned_data.get("foto")
        # só valida upload novo (arquivo já salvo não tem content_type)
        if foto and hasattr(foto, "content_type"):
            if foto.content_type not in FORMATOS_FOTO:
                raise forms.ValidationError("Envie a foto em JPEG, PNG ou WebP.")
            if foto.size > TAMANHO_MAX_FOTO:
                raise forms.ValidationError("A foto pode ter no máximo 5 MB.")
        return foto
        
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

class DenunciaForm(forms.ModelForm):
    class Meta:
        model = Denuncia
        fields = ["motivo", "detalhe"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["cf-turnstile-response"] = TurnstileField()

    