from decimal import Decimal
from time import sleep

from scraper.models import Produto
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By


def buscar_produtos_mercado_livre(nome_produto: str):
    Produto.objects.filter(fonte="mercadolivre").delete()

    chrome_options = Options()
    chrome_options.add_argument("window-size=1200,1000")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument(
        "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    )

    navegador = webdriver.Chrome(options=chrome_options)

    navegador.get("https://www.mercadolivre.com.br/")
    sleep(3)

    campo_busca = navegador.find_element(By.ID, "cb1-edit")
    campo_busca.send_keys(nome_produto)
    campo_busca.submit()

    sleep(3)

    # Scrolla aos poucos para carregar as imagens com lazy-load
    for i in range(0, 10):
        navegador.execute_script(f"window.scrollBy(0, {i * 500});")
        sleep(1)

    sleep(2)

    produtos_html = navegador.find_elements(By.CLASS_NAME, "ui-search-layout__item")

    for produto in produtos_html:
        try:
            # Título
            try:
                titulo_element = produto.find_element(By.CSS_SELECTOR, "h3")
                titulo = titulo_element.text.strip()
            except Exception as e:
                print(f"Erro ao encontrar título: {e}")
                continue

            # Link
            try:
                link_element = produto.find_element(By.CSS_SELECTOR, "a")
                link = link_element.get_attribute("href")
            except Exception as e:
                print(f"Erro ao encontrar link: {e}")
                continue

            # Valor
            try:
                valor_inteiro = (
                    produto.find_element(By.CLASS_NAME, "andes-money-amount__fraction")
                    .text.strip()
                    .replace(".", "")
                    .replace(",", "")
                )
            except Exception as e:
                print(f"Erro ao encontrar valor inteiro: {e}")
                valor_inteiro = "0"

            try:
                valor_decimal = produto.find_element(
                    By.CLASS_NAME, "andes-money-amount__cents"
                ).text.strip()
            except Exception as e:
                print(f"Erro ao encontrar valor decimal: {e}")
                valor_decimal = "00"
                continue

            valor_completo_texto = f"{valor_inteiro}.{valor_decimal}"
            valor = Decimal(valor_completo_texto)

            # Imagem
            try:
                img_element = produto.find_element(By.TAG_NAME, "img")
                imagem_url = img_element.get_attribute("src")

                # Se for imagem base64 (placeholder), tenta pegar o data-src
                if imagem_url.startswith("data:image"):
                    imagem_url = img_element.get_attribute("data-src") or ""
            except:
                imagem_url = ""

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
