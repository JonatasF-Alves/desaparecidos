from django.urls import path
from . import views

app_name = "analises"
urlpatterns = [path("", views.painel, name="painel")]
