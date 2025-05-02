from django.contrib import admin
from django.urls import path

from .view import pagina_inicial_view, pagina_resultado_consulta_view

app_name = "scraper"
urlpatterns = [
    path("resultado_busca", pagina_resultado_consulta_view.pagina_resultado_view, name="resultado"),
    path("inicio", pagina_inicial_view.pagina_inicial_view, name="inicio"),
]
