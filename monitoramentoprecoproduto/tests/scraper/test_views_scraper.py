from http import HTTPStatus
from unittest.mock import patch

import pytest
from bs4 import BeautifulSoup
from django.contrib.auth.models import User
from django.urls import reverse
from scraper.models import Produto
from scraper.view import pagina_inicial_view, pagina_resultado_consulta_view


@pytest.mark.django_db
def test_view_pagina_inicial(client):
    user = User.objects.create_user(username="testuser", password="testpassword")
    client.force_login(user)

    url = reverse("scraper:inicio")
    response = client.get(url)

    template_usado = [t.name for t in response.templates]

    # Verifica se o template correto está sendo usado
    assert "scraper/pagina_inicial.html" in template_usado
    # Verifica se o status da resposta é 200 (OK)
    assert response.status_code == HTTPStatus.OK
    # Verifica se o nome da url corresponde ao nome esperado
    assert response.resolver_match.view_name == "scraper:inicio"
    # Verifica se a view correspondente é a esperada
    assert response.resolver_match.func == pagina_inicial_view.pagina_inicial_view


@pytest.mark.django_db
def test_view_pagina_resultado_consulta(client):
    user = User.objects.create_user(username="testuser", password="testpassword")
    client.force_login(user)

    dados_enviados = {
        "valor_buscado": "Produto Teste",
        "loja": "mercadolivre,buscape",
        "categoria": "Categoria Teste",
    }

    # Criar os produtos para simular o banco de dados
    dados_retornados_buscape = Produto.objects.create(
        titulo="Produto Teste",
        valor=100.00,
        link="http://example.com/produto-teste",
        imagem_url="http://example.com/imagem-teste.jpg",
        data="2023-10-01T12:00:00Z",
        fonte="buscape",
    )

    dados_retornados_mercadolivre = Produto.objects.create(
        titulo="Produto Teste",
        valor=100.00,
        link="http://example.com/produto-teste",
        imagem_url="http://example.com/imagem-teste.jpg",
        data="2023-10-01T12:00:00Z",
        fonte="mercadolivre",
    )

    resultado_falso_buscape = {"buscape": [dados_retornados_buscape]}
    resultado_falso_mercadolivre = {"mercadolivre": [dados_retornados_mercadolivre]}

    # Patch nas funções de busca
    with (
        patch(
            "scraper.view.pagina_resultado_consulta_view.buscar_produtos_buscape",
            return_value=resultado_falso_buscape,
        ) as mock_buscape,
        patch(
            "scraper.view.pagina_resultado_consulta_view.buscar_produtos_mercado_livre",
            return_value=resultado_falso_mercadolivre,
        ) as mock_mercadolivre,
    ):
        url = reverse("scraper:resultado")
        response = client.get(url, data=dados_enviados)

        assert response.status_code == HTTPStatus.OK

        mock_buscape.assert_called_once()
        mock_mercadolivre.assert_called_once()

        # Parse do conteúdo da resposta
        soup = BeautifulSoup(response.content, "html.parser")

        # Verificar produtos na resposta
        lista_produtos = soup.find_all("li", class_="produto")
        assert len(lista_produtos) > 0  # Verifica se ao menos um produto foi retornado

        # Testar cada produto individualmente
        for produto in lista_produtos:
            validar_produto(produto)


# Função auxiliar para validações de um produto
def validar_produto(produto):
    # Título do produto
    titulo_produto = produto.find("strong", class_="titulo-produto").get_text(
        strip=True
    )
    assert "Produto Teste" in titulo_produto

    # Preço do produto
    preco_produto = produto.find("div", class_="preco").get_text(strip=True)
    assert "Preço: 100,00" in preco_produto

    # Fonte de pesquisa
    fonte_produto = produto.find("p", class_="fonte-de-pesquisa").get_text(strip=True)
    assert fonte_produto in ["buscape", "mercadolivre"]

    # URL do produto
    url_produto = produto.find("a", href=True)["href"]
    assert "http://example.com/produto-teste" in url_produto

    # URL da imagem
    imagem_produto = produto.find("img", class_="imagem-produto")["src"]
    assert "http://example.com/imagem-teste.jpg" in imagem_produto
