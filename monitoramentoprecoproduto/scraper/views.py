from django.shortcuts import render
from scraper.scraping import buscar_produtos

from .models import Produto


def scrape_view(request):
    termo = request.GET["q"]
    buscar_produtos(termo)
    produtos = Produto.objects.all()
    return render(
        request, "scraper/pagina_resultado_busca.html", {"produtos": produtos}
    )


def home_page_view(request):
    return render(request, "scraper/pagina_inicial.html")
