class ErroDeExtracao(Exception):
    """Levantado quando não é possível extrair os dados esperados da página."""


class BaseScraper:
    """Contrato de todo coletor de loja."""

    def extrair(self, html):
        """Recebe o HTML da página (texto) e devolve um dicionário com:

        - nome: nome do produto (texto)
        - preco_vista_centavos: preço à vista, em centavos (inteiro)
        - preco_cheio_centavos: preço cheio, em centavos (inteiro)
        - disponivel: True se o produto está disponível para compra

        Se não conseguir extrair, levanta ErroDeExtracao.
        """
        raise NotImplementedError("Cada loja precisa implementar extrair()")