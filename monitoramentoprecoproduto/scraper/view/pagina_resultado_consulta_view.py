from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
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

        if not termo.strip() or lojas == [""] or lojas == []:
            return redirect("scraper:inicio")

        if "mercadolivre" in lojas:
            buscar_produtos_mercado_livre(categoria or termo)   

        if "buscape" in lojas:
            buscar_produtos_buscape(categoria or termo)

        produtos_lista = Produto.objects.filter(fonte__in=lojas)
        contexto = {"produtos": produtos_lista}

    except Exception as e:
        raise Http404(f"Erro: {e}")

    return render(request, "scraper/pagina_resultado_busca.html", contexto)
