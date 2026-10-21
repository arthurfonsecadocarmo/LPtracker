# Spike 01 — Leitura de preço da Kabum a partir do GitHub Actions

**Data:** 2026-10-20 (noite, 22:00)
**Código:** `src/spike.py` e `.github/workflows/spike.yml`

## Pergunta
Um runner do GitHub Actions (IP de datacenter) consegue ler o preço de um produto da Kabum usando apenas `requests` + `BeautifulSoup`?

## Método
Script que faz uma única requisição à página de um produto (RX 7600 ASRock Challenger Pro OC, código 907814) e testa três estratégias de extração: JSON-LD, `__NEXT_DATA__` e expressão regular. Executado localmente e no GitHub Actions (disparo manual).

Ambiente da execução na nuvem: Ubuntu 24.04 (Azure, região eastus), Python 3.14.7, `requests` 2.34.2, `beautifulsoup4` 4.15.0.

## Resultado
- **Status HTTP 200** no runner, com HTML de ~120 mil caracteres.
- `__NEXT_DATA__` contém os preços em campos numéricos:

| Campo | Valor na execução | Significado |
|---|---|---|
| `product.prices.priceWithDiscount` | 1959.99 | Preço à vista (PIX) |
| `product.prices.price` | 2305.87 | Preço cheio |
| `product.prices.oldPrice` | 2941.16 | Preço "riscado" (marketing), ignorado |

- JSON-LD traz o nome do produto (`@type: Product`); a saída foi truncada e a presença de preço ainda não foi verificada.
- A regex encontrou os mesmos valores como texto (`R$ 2.941,16`, `R$ 1.959,99`, `R$ 230,58`).

## Conclusão
Viável sem Playwright. Estratégia principal: `__NEXT_DATA__`; reserva: JSON-LD.

## Riscos e pendências
- O caminho dos campos é interno ao site e pode mudar sem aviso.
- Apenas uma execução na nuvem até agora: repetir em outros horários para detectar bloqueios intermitentes.
- Verificar se o JSON-LD inclui preço (`offers`), como fonte reserva.

## Decisões derivadas
- Preço rastreado: `preco_vista` e `preco_cheio` (ADR 6).
- Estratégia de coleta registrada no ADR 2.