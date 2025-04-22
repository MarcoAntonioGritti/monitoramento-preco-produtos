from decimal import Decimal, InvalidOperation
from time import sleep

from bs4 import BeautifulSoup
from scraper.models import Produto
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


def buscar_produtos_mercado_livre(nome_produto: str):
    # Excluindo os dados antigos do banco de dados
    Produto.objects.filter(fonte="mercadolivre").delete()

    # Configurações do Selenium para o Chrome
    chrome_options = Options()
    chrome_options.add_argument("window-size=600,800")
    chrome_options.add_argument(
        "--headless"
    )  # Comente essa linha se quiser ver o navegador
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    navegador = webdriver.Chrome(options=chrome_options)

    # Acessa o site do Mercado Livre
    navegador.get("https://www.mercadolivre.com.br/")
    sleep(3)

    # Preenche o campo de busca
    campo_busca = navegador.find_element(By.ID, "cb1-edit")
    campo_busca.send_keys(nome_produto)
    campo_busca.submit()

    # Aguarda e faz scroll pra carregar as imagens
    sleep(3)
    navegador.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(3)

    # Captura os blocos de produtos usando Selenium
    produtos_html = navegador.find_elements(By.CLASS_NAME, "ui-search-layout__item")

    for produto in produtos_html:
        try:
            # Título
            titulo_element = produto.find_element(By.CSS_SELECTOR, "h3")
            titulo = titulo_element.text.strip()

            # Link
            link_element = produto.find_element(By.CSS_SELECTOR, "a")
            link = link_element.get_attribute("href")

            # Valor
            valor_inteiro = (
                produto.find_element(By.CLASS_NAME, "andes-money-amount__fraction")
                .text.strip()
                .replace(".", "")
                .replace(",", "")
            )
            try:
                valor_decimal = produto.find_element(
                    By.CLASS_NAME, "andes-money-amount__cents"
                ).text.strip()
            except:
                valor_decimal = "00"
            valor_completo_texto = f"{valor_inteiro}.{valor_decimal}"
            valor = Decimal(valor_completo_texto)

            # Imagem
            try:
                img_element = produto.find_element(By.TAG_NAME, "img")
                imagem_url = (
                    img_element.get_attribute("src")
                    or img_element.get_attribute("data-src")
                    or ""
                )
            except:
                imagem_url = ""

            # Cria produto no banco
            Produto.objects.create(
                titulo=titulo,
                valor=valor,
                link=link,
                imagem_url=imagem_url,
                fonte="mercadolivre",
            )

        except Exception as e:
            print(f"Erro ao processar produto: {e}")

    navegador.quit()
