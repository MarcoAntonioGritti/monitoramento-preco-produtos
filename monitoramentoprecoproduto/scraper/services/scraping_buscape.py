from decimal import Decimal, InvalidOperation
from time import sleep

from bs4 import BeautifulSoup
from scraper.models import Produto
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def buscar_produtos_buscape(nome_produto: str):
    # Limpa os produtos antigos da fonte Buscapé
    Produto.objects.filter(fonte="buscape").delete()

    # Configurações do navegador (headless + user-agent)
    chrome_options = Options()
    chrome_options.add_argument("window-size=1200,1000")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64)")
    chrome_options.add_argument("--headless")

    navegador = webdriver.Chrome(options=chrome_options)
    navegador.get("https://www.buscape.com.br/")
    sleep(3)

    # Busca pelo produto
    try:
        campo_busca = navegador.find_element(
            By.CSS_SELECTOR, "input[data-test='input-search']"
        )
        campo_busca.send_keys(nome_produto)
        campo_busca.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Erro ao buscar produto: {e}")
        navegador.quit()
        return

    sleep(5)  # Dá tempo para a página de resultados carregar completamente

    soup = BeautifulSoup(navegador.page_source, "html.parser")

    produtos_html = soup.select("div.ProductCard_ProductCard__WWKKW")
    precos_html = soup.select("p.Text_MobileHeadingS__HEz7L")
    imagens_html = soup.select(".ProductCard_ProductCard_Image__4v1sa img")

    for produto_html, preco_html, imagem_html in zip(
        produtos_html, precos_html, imagens_html
    ):
        try:
            titulo_element = produto_html.select_one(
                "h2.ProductCard_ProductCard_Name__U_mUQ"
            )
            if not titulo_element:
                continue
            titulo = titulo_element.text.strip()

            try:
                preco_texto = preco_html.text.strip()
                preco_formatado = (
                    preco_texto.replace("R$", "").replace(".", "").replace(",", ".")
                )
                valor = Decimal(preco_formatado)

            except Exception as e:
                print(f"Erro ao processar valor: {e}")
                valor = Decimal(0)
                continue

            try:
                link_element = produto_html.select_one(
                    "a.ProductCard_ProductCard_Inner__gapsh"
                )
                link = "https://www.buscape.com.br" + link_element["href"]
            except (AttributeError, TypeError):
                link = ""

            imagem_url = imagem_html.get("src", "") if imagem_html else ""

            Produto.objects.create(
                titulo=titulo,
                valor=valor,
                link=link,
                imagem_url=imagem_url,
                fonte="buscape",
            )

        except (InvalidOperation, AttributeError, TypeError) as e:
            print(f"Erro ao processar produto: {e}")
        except Exception as e:
            print(f"Erro inesperado: {e}")

    navegador.quit()
