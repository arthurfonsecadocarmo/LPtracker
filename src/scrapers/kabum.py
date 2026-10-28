import json

from bs4 import BeautifulSoup

from scrapers.base import BaseScraper, ErroDeExtracao


def para_centavos(valor):
    """Converte reais (float) em centavos (int), arredondando."""
    return round(valor * 100)


class KabumScraper(BaseScraper):
    def extrair(self, html):
        soup = BeautifulSoup(html, "html.parser")

        # 1. Achar o bloco de dados que o Next.js embute na página
        tag = soup.find("script", id="__NEXT_DATA__")
        if tag is None or not tag.string:
            raise ErroDeExtracao("Bloco __NEXT_DATA__ não encontrado na página")

        # 2. Converter o texto JSON em dicionário
        try:
            dados = json.loads(tag.string)
        except json.JSONDecodeError as erro:
            raise ErroDeExtracao(f"__NEXT_DATA__ não é um JSON válido: {erro}")

        # 3. Entrar no dicionário com .get(), sem estourar KeyError
        produto = dados.get("props", {}).get("pageProps", {}).get("product")
        if not produto:
            raise ErroDeExtracao("Produto não encontrado em props.pageProps.product")

        precos = produto.get("prices") or {}
        nome = produto.get("title")
        preco_vista = precos.get("priceWithDiscount")
        preco_cheio = precos.get("price")

        # 4. Conferir que tudo o que precisamos existe e faz sentido
        if not nome:
            raise ErroDeExtracao("Nome do produto (title) ausente")
        for rotulo, valor in (("priceWithDiscount", preco_vista), ("price", preco_cheio)):
            if not isinstance(valor, (int, float)) or valor <= 0:
                raise ErroDeExtracao(f"Preço inválido ou ausente em prices.{rotulo}: {valor!r}")

        # 5. Devolver no formato do contrato (preços em centavos)
        return {
            "nome": nome,
            "preco_vista_centavos": para_centavos(preco_vista),
            "preco_cheio_centavos": para_centavos(preco_cheio),
            "disponivel": bool(produto.get("available", True)),
        }
