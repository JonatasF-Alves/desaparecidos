from django import forms
from .models import Caso


class CasoForm(forms.ModelForm):
    class Meta:
        model = Caso
        fields = ["nome", "idade", "foto", "cidade", "estado",
                  "data_desaparecimento", "descricao", "contato", "numero_bo"]
        widgets = {"data_desaparecimento": forms.DateInput(attrs={"type": "date"})}
