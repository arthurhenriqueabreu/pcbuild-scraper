import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configura o driver Chrome (garanta que chromedriver está no PATH)
driver = webdriver.Chrome()

urls = {
    "cpu": "https://www.pcbuildwizard.com/product/cpu",
    "gpu": "https://www.pcbuildwizard.com/product/video-card",
    "ram": "https://www.pcbuildwizard.com/product/memory",
    "motherboard": "https://www.pcbuildwizard.com/product/motherboard",
    "storage": "https://www.pcbuildwizard.com/product/ssd",
    "powersupply": "https://www.pcbuildwizard.com/product/power-supply",
    "case": "https://www.pcbuildwizard.com/product/case"
}

if not os.path.exists("data"):
    os.mkdir("data")

for category, url in urls.items():
    print(f"Visitando categoria: {category} - {url}")
    driver.get(url)

    try:
        # Espera até que pelo menos um produto seja carregado na página
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.description-cell"))
        )

        # Busca todos os nomes e preços
        nomes = driver.find_elements(By.CSS_SELECTOR, "span.description-cell")
        precos = driver.find_elements(By.CSS_SELECTOR, "td.price-cell.mud-table-cell")

        if len(nomes) != len(precos):
            print(f"Atenção: número diferente de nomes ({len(nomes)}) e preços ({len(precos)}) na categoria {category}")

        produtos = []
        for nome, preco in zip(nomes, precos):
            produtos.append(f"{nome.text.strip()} - {preco.text.strip()}")

        caminho_arquivo = f"data/{category}.txt"
        with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
            arquivo.write("\n".join(produtos))

        print(f"Salvo {len(produtos)} produtos em {caminho_arquivo}")

    except Exception as e:
        print(f"Erro na categoria {category}: {e}")

driver.quit()
