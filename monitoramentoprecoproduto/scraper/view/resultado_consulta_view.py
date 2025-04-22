from django.http import HttpResponse
from django.template import loader
from scraper.models import Produto

from ..services.scraping_buscape import buscar_produtos_buscape
from ..services.scraping_mercado_livre import buscar_produtos_mercado_livre


def resultado_view(request):
    termo = request.GET["valor_buscado"]
    lojas = request.GET.get("loja", "").split(",")

    if "mercadolivre" in lojas:
        buscar_produtos_mercado_livre(termo)
    elif "buscape" in lojas:
        buscar_produtos_buscape(termo)
    else:
        print("Loja não reconhecida ou botão não foi clicado corretamente.")

    produtos_lista = Produto.objects.all()

    template = loader.get_template("scraper/pagina_resultado_busca.html")

    contexto = {"produtos": produtos_lista}

    return HttpResponse(template.render(contexto, request))
