from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import time
import os

# Inicializar Selenium (modo headless opcional)
options = Options()
options.add_argument('--headless')  # Remova essa linha se quiser ver o navegador
driver = webdriver.Chrome(options=options)

categorias = {
    "cpu": "https://www.pcbuildwizard.com/product/cpu",
    "gpu": "https://www.pcbuildwizard.com/product/video-card",
    "ram": "https://www.pcbuildwizard.com/product/memory",
    "motherboard": "https://www.pcbuildwizard.com/product/motherboard",
    "storage": "https://www.pcbuildwizard.com/product/ssd",
    "powersupply": "https://www.pcbuildwizard.com/product/power-supply",
    "case": "https://www.pcbuildwizard.com/product/case"
}

# Criar pasta de saída
os.makedirs("data_json", exist_ok=True)

# Função para limpar e converter preço para float
def preco_para_float(preco_str):
    preco_limpo = preco_str.replace("R$", "").replace(".", "").replace(",", ".").strip()
    try:
        return float(preco_limpo)
    except:
        return None

# Dicionário com todos os produtos
dados_completos = {}

for categoria, url in categorias.items():
    print(f"\n🔎 Visitando categoria: {categoria} - {url}")
    driver.get(url)
    time.sleep(2)

    # Scroll até que todos os produtos sejam carregados
    prev_count = -1
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        linhas = driver.find_elements(By.CSS_SELECTOR, "tr.mud-table-row")
        if len(linhas) == prev_count:
            break
        prev_count = len(linhas)

    print(f"📦 {len(linhas)} produtos encontrados")

    produtos = []
    for linha in linhas:
        try:
            nome = linha.find_element(By.CSS_SELECTOR, ".description-cell").text.strip()
        except:
            nome = ""

        try:
            detalhes = linha.find_element(By.CSS_SELECTOR, ".details-cell").text.strip()
        except:
            detalhes = ""

        try:
            precos = linha.find_elements(By.CSS_SELECTOR, ".price-cell")
            preco_avista = preco_para_float(precos[0].text.strip()) if len(precos) > 0 else None
            preco_parcelado = preco_para_float(precos[1].text.strip()) if len(precos) > 1 else None
            parcelas = precos[2].text.strip() if len(precos) > 2 else ""
        except:
            preco_avista = preco_parcelado = None
            parcelas = ""

        try:
            cupom = linha.find_element(By.CSS_SELECTOR, '[data-label="Cupom"]').text.strip()
        except:
            cupom = ""

        produto = {
            "Nome": nome,
            "Detalhes": detalhes,
            "Preco_avista": preco_avista,
            "Preco_parcelado": preco_parcelado,
            "Parcelas": parcelas,
            "Cupom": cupom
        }

        produtos.append(produto)

    dados_completos[categoria] = produtos
    print(f"✅ Salvo {len(produtos)} produtos da categoria {categoria}")

# Salvar em JSON
json_path = "data_json/produtos_pcbuildwizard.json"
with open(json_path, "w", encoding="utf-8") as f:
    json.dump(dados_completos, f, indent=2, ensure_ascii=False)

print(f"\n💾 Dados salvos em: {json_path}")
driver.quit()
