from django.urls import path
from . import views

app_name = "casos"

urlpatterns = [
    path("", views.CasoListView.as_view(), name="lista"),
    path("caso/<int:pk>/", views.CasoDetailView.as_view(), name="detalhe"),
    path("cadastrar/", views.CasoCreateView.as_view(), name="cadastrar"),
    path("meus-casos/", views.MeusCasosView.as_view(), name="meus_casos"),
]
