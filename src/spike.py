import json
import re

import requests
from bs4 import BeautifulSoup

URL = "https://www.kabum.com.br/produto/907814/placa-de-video-asrock-rx-7600-challenger-pro-oc-amd-radeon-8gb-gddr6-triple-fan-90-ga62zz-00uanf"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "pt-BR,pt;q=0.9",
}

resp = requests.get(URL, headers=HEADERS, timeout=20)
print("Status:", resp.status_code)
print("Tamanho do HTML:", len(resp.text), "caracteres")

soup = BeautifulSoup(resp.text, "html.parser")

# Tentativa 1: dados estruturados (JSON-LD)
for tag in soup.find_all("script", type="application/ld+json"):
    print("[JSON-LD]", (tag.string or "")[:500])


# Tentativa 2: dados embutidos pelo Next.js
def achar_precos(obj, caminho=""):
    achados = []
    if isinstance(obj, dict):
        for chave, valor in obj.items():
            novo = f"{caminho}.{chave}"
            if any(p in chave.lower() for p in ("price", "preco")) and isinstance(valor, (int, float, str)):
                achados.append((novo, valor))
            achados += achar_precos(valor, novo)
    elif isinstance(obj, list):
        for i, item in enumerate(obj):
            achados += achar_precos(item, f"{caminho}[{i}]")
    return achados


next_data = soup.find("script", id="__NEXT_DATA__")
if next_data and next_data.string:
    print("[NEXT_DATA] encontrado")
    for caminho, valor in achar_precos(json.loads(next_data.string))[:30]:
        print("  ", caminho, "=", valor)
else:
    print("[NEXT_DATA] não encontrado")

# Tentativa 3: procurar "R$ 1.234,56" no texto
print("[REGEX]", re.findall(r"R\$\s?[\d.]+,\d{2}", resp.text)[:10])