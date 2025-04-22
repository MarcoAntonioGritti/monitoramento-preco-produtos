from decimal import Decimal, InvalidOperation
from time import sleep

import pandas as pd
from bs4 import BeautifulSoup
from scraper.models import Produto
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def buscar_produtos_buscape(nome_produto: str):
    # Excluindo os dados antigos do banco de dados
    Produto.objects.filter(fonte="buscape").delete()

    # Configurações do Selenium para o Chrome
    chrome_options = Options()
    chrome_options.add_argument("window-size=600,800")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    chrome_options.add_argument(
        "--headless"
    )  # Argumento que serve para rodar o navegador em segundo plano(opcional)

    navegador = webdriver.Chrome(options=chrome_options)

    # Inicia o navegador e acessa o site do Buscapé
    navegador.get("https://www.buscape.com.br/")

    # Aguarda o carregamento da página
    sleep(3)

    # Localiza o campo de busca e insere o nome do produto
    campo_busca = navegador.find_element(
        By.CSS_SELECTOR, ("input[data-test='input-search']")
    )
    campo_busca.send_keys(nome_produto)
    campo_busca.send_keys(Keys.ENTER)

    # Obtendo o conteúdo da página
    pagina_html = BeautifulSoup(navegador.page_source, "html.parser")

    lista_produtos = pagina_html.find_all(
        "div",
        class_="Paper_Paper__4XALQ Paper_Paper__bordered__cl5Rh Card_Card__Zd8Ef Card_Card__clicable__ewI68 ProductCard_ProductCard__WWKKW",
    )

    lista_precos = pagina_html.find_all(
        "p", class_="Text_Text__ARJdp Text_MobileHeadingS__HEz7L"
    )

    imagens = pagina_html.select(".ProductCard_ProductCard_Image__4v1sa img")

    for preco_html, produto_html, imagem in zip(lista_precos, lista_produtos, imagens):

        titulo_produto = produto_html.find(
            "h2",
            class_="Text_Text__ARJdp Text_MobileLabelXs__dHwGG Text_DesktopLabelSAtLarge__wWsED ProductCard_ProductCard_Name__U_mUQ",
        )

        preco_texto = preco_html.text

        preco_formatado = (
            preco_texto.replace("R$", "").replace(".", "").replace(",", ".").strip()
        )

        preco_decimal = Decimal(preco_formatado)

        link_elemento = produto_html.find(
            "a", class_="ProductCard_ProductCard_Inner__gapsh"
        )

        link_completo = "https://www.buscape.com.br" + link_elemento["href"]

        img = imagem["src"]

        if titulo_produto and preco_decimal:
            try:
                Produto.objects.create(
                    titulo=titulo_produto.text.strip(),
                    valor=preco_decimal,
                    link=link_completo,
                    imagem_url=img,
                    fonte="buscape",
                )
            except Exception as e:
                print(f"Erro ao salvar o produto: {e}")
            except (InvalidOperation, AttributeError) as e:
                print(f"Erro ao processar o valor do produto: {e}")

    navegador.quit()
