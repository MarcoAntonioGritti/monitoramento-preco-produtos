from django.contrib import admin
from django.urls import path

from .view import pagina_inicial_view, resultado_consulta_view

urlpatterns = [
    path("scrape/", resultado_consulta_view.resultado_view, name="resultado"),
    path("", pagina_inicial_view.pagina_inicial_view, name="inicio"),
]
