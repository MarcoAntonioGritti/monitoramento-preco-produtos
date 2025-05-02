from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render
from scraper.models import Produto

from ..services.scraping_buscape import buscar_produtos_buscape
from ..services.scraping_mercado_livre import buscar_produtos_mercado_livre


@login_required
def pagina_resultado_view(request):
    try:
        termo = request.GET.get("valor_buscado", "")
        lojas = request.GET.get("loja", "").split(",")
        categoria = request.GET.get("categoria", "")

        lojas = [loja.strip().lower() for loja in lojas]

        if "mercadolivre" in lojas:
            if categoria:
                termo = categoria
                buscar_produtos_mercado_livre(termo)
            else:
                buscar_produtos_mercado_livre(termo)
        if "buscape" in lojas:
            if categoria:
                termo = categoria
                buscar_produtos_buscape(termo)
            else:
                buscar_produtos_buscape(termo)
        if not lojas or lojas == [""]:
            print("Nenhuma loja foi selecionada.")

        # Filtra os produtos com base nas lojas selecionadas
        produtos_lista = Produto.objects.filter(fonte__in=lojas)

        contexto = {"produtos": produtos_lista}
    except Exception as e:
        raise Http404(f"Erro: {e}")

    return render(request, "scraper/pagina_resultado_busca.html", contexto)
