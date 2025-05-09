import pytest
from scraper.models import Produto


@pytest.mark.django_db
def test_criacao_produto():

    # Given
    titulo = "Produto Teste"
    valor = 99.99
    link = "http://example.com/produto-teste"
    imagem_url = "http://example.com/imagem-teste.jpg"
    fonte = "Fonte Teste"

    # When
    produto = Produto.objects.create(
        titulo=titulo, valor=valor, link=link, imagem_url=imagem_url, fonte=fonte
    )

    produtos_count = Produto.objects.all().count()

    assert produtos_count == 1
    assert produto.titulo == titulo
    assert produto.valor == valor
    assert produto.link == link
    assert produto.imagem_url == imagem_url
    assert produto.fonte == fonte
