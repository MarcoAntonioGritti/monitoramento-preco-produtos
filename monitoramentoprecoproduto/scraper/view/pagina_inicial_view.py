from django.shortcuts import render
from scraper.models import Produto

from ..services.scraping_buscape import buscar_produtos_buscape
from ..services.scraping_mercado_livre import buscar_produtos_mercado_livre


def pagina_inicial_view(request):
    return render(request, "scraper/pagina_inicial.html")
