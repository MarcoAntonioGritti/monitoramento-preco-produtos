from decimal import Decimal, InvalidOperation
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from scraper.models import Produto
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def buscar_produtos(nome_do_produto: str):
    # Excluindo os dados antigos do banco de dados
    Produto.objects.all().delete()

    # Configurações do Selenium para o Chrome
    options = Options()
    options.add_argument("window-size=600,800")
    # options.add_argument("--headless")  # descomente(opcional)

    navegador = webdriver.Chrome(options=options)

    # Inicia o navegador e acessa o site do Mercado Livre
    navegador.get("https://www.mercadolivre.com.br/")

    # Aguarda o carregamento da página
    sleep(3)

    # Localiza o campo de busca e insere o nome do produto
    input_product = navegador.find_element(By.ID, "cb1-edit")
    input_product.send_keys(nome_do_produto)
    input_product.submit()

    # Obtendo o conteúdo da página
    site = BeautifulSoup(navegador.page_source, "html.parser")

    produtos = site.findAll("h3", class_="poly-component__title-wrapper")
    div_valor_produto = site.findAll("div", class_="poly-price__current")

    for produto, preco in zip(produtos, div_valor_produto):
        titulo = produto.find("a", class_="poly-component__title")
        valor_inteiro = preco.find("span", class_="andes-money-amount__fraction")
        valor_decimal = preco.find(
            "span",
            class_="andes-money-amount__cents andes-money-amount__cents--superscript-24",
        )

        if titulo and valor_inteiro:
            try:
                # Verifica e converte o valor para Decimal
                valor_texto_completo = f"{valor_inteiro.text.strip()}.{valor_decimal.text.strip() if valor_decimal else '00'}"
                valor_atual = Decimal(valor_texto_completo)
                try:
                    Produto.objects.create(
                        titulo=titulo.text.strip(),
                        valor=valor_atual,
                        link=titulo["href"],
                    )
                except Exception as e:
                    print(f"Erro ao salvar o produto: {e}")
            except (InvalidOperation, AttributeError) as e:
                print(f"Erro ao processar o valor do produto: {e}")

    navegador.quit()
