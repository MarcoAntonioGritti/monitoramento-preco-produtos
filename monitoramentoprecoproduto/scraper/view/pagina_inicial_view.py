from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def pagina_inicial_view(request):
    return render(request, "scraper/pagina_inicial.html")
