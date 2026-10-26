from django.contrib import admin
from .models import Caso


@admin.action(description="Aprovar casos selecionados")
def aprovar(modeladmin, request, queryset):
    queryset.update(aprovado=True)


@admin.register(Caso)
class CasoAdmin(admin.ModelAdmin):
    list_display = ("nome", "cidade", "status", "aprovado", "criado_em")
    list_filter = ("aprovado", "status", "estado")
    list_editable = ("aprovado", "status")
    search_fields = ("nome", "cidade", "numero_bo")
    actions = [aprovar]
