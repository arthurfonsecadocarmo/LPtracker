from pathlib import Path

import pytest

from scrapers.base import ErroDeExtracao
from scrapers.kabum import KabumScraper

FIXTURE = Path(__file__).parent / "fixtures" / "kabum_907814.html"


def test_extrai_nome_e_precos_da_pagina_salva():
    html = FIXTURE.read_text(encoding="utf-8")

    dados = KabumScraper().extrair(html)

    assert dados["nome"].startswith("Placa de Vídeo ASRock RX 7600")
    assert dados["preco_vista_centavos"] == 199999
    assert dados["preco_cheio_centavos"] == 235293
    assert dados["disponivel"] is True


def test_pagina_sem_next_data_levanta_erro():
    with pytest.raises(ErroDeExtracao):
        KabumScraper().extrair("<html><body>nada aqui</body></html>")


def test_json_invalido_levanta_erro():
    html = '<script id="__NEXT_DATA__" type="application/json">{quebrado</script>'
    with pytest.raises(ErroDeExtracao):
        KabumScraper().extrair(html)


def test_preco_ausente_levanta_erro():
    html = (
        '<script id="__NEXT_DATA__" type="application/json">'
        '{"props": {"pageProps": {"product": {"title": "X", "prices": {}}}}}'
        "</script>"
    )
    with pytest.raises(ErroDeExtracao):
        KabumScraper().extrair(html)
