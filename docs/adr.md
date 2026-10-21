# Architecture Decision Records (ADR)

Cada decisão tem um status: **Proposta** (ainda não validada) → **Aceita** (validada ou assumida) → **Substituída** (trocada por outra decisão).

Última revisão: 2026-10-20

---

## 1. Automação
- **Status:** Aceita (executa na nuvem, validado no [Spike 01](spikes/01-kabum.md)).
- **Decisão:** GitHub Actions (cron job a cada 12 horas), com disparo manual (`workflow_dispatch`) para testes.
- **Razão:** Viabilizar o projeto mantendo o custo zero, atendendo às restrições de infraestrutura.
- **Trade-offs:**
  - Limitação do tempo máximo de execução por job.
  - O agendamento não é pontual: atrasos de alguns minutos são normais.
  - O runner é **efêmero** (nasce limpo a cada execução). Consequência tratada no ADR 3.
  - Em repositórios sem atividade por muito tempo, o GitHub pode desativar workflows agendados.
- **Manutenção:** fixar `runs-on: ubuntu-24.04` (em vez de `ubuntu-latest`, que muda sozinho) e atualizar as actions (`checkout`, `setup-python`) quando as versões atuais forem confirmadas, pois o Node.js 20 está deprecado.

## 2. Coletor (Scraper Isolado)
- **Status:** Aceita (validada no [Spike 01](spikes/01-kabum.md)).
- **Decisão:** Requisição HTTP pura (`requests` + `BeautifulSoup`). Playwright fica como plano B, apenas se um site alvo exigir JavaScript.
- **Fonte de dados na página (Kabum):**
  1. Principal: bloco `__NEXT_DATA__` (JSON embutido pelo Next.js), com preços numéricos.
  2. Reserva: JSON-LD (schema.org `Product`), a ser verificado quanto à presença de preço.
  3. Último recurso: expressão regular sobre o texto da página.
- **Razão:** Otimizar performance e consumo de recursos. Ler dados estruturados é mais estável do que depender do layout visual.
- **Trade-off:** O caminho dos campos (`props.pageProps.product.prices...`) é interno ao site e pode mudar sem aviso. Mitigações: código de extração isolado do restante, testes com HTML salvo (fixtures) e alerta de falha (ver SRS).

## 3. Armazenamento (Banco de Dados)
- **Status:** - **Status:** Aceita (validada no [Spike 02](spikes/02-persistencia.md)).
- **Decisão:** SQLite (`data/tracker.db`), **persistido no próprio repositório**: ao fim de cada execução, o workflow faz commit e push do banco atualizado; na execução seguinte, o `checkout` já traz o histórico.
- **Razão:** Armazenamento local estruturado, sem burocracia de servidores, com suporte a SQL nativo e custo zero. O repositório funciona como "armário" entre execuções, já que o runner é efêmero.
- **Requisitos do workflow:** permissão `contents: write` e `concurrency` (para impedir duas execuções simultâneas corrompendo o arquivo).
- **Alternativas descartadas por ora:**
  - `actions/cache` ou artifacts: podem expirar ou ser descartados, e o histórico precisa durar 90 dias.
  - Banco hospedado (ex.: Turso, Supabase): resolve a persistência, mas adiciona dependência externa e mais segredos.
- **Trade-offs:** O arquivo binário cresce e o Git guarda cada versão (irrelevante no volume esperado). Não é ideal para escrita concorrente em altíssima escala (o que não é o nosso caso).
- **Convenções de dados:** preços armazenados em **centavos (inteiro)**; timestamps em **UTC** (ISO 8601).

## 4. Processamento & Regra de Negócio
- **Status:** Proposta (parâmetros a definir).
- **Preço de referência:** `preco_vista` (à vista/PIX). O `preco_cheio` é guardado como informação adicional (ver ADR 6).
- **Lógica:** Consulta o menor valor histórico do produto nos últimos 90 dias, **excluindo a coleta atual**.
- **Condição de alerta:** Preço atual <= menor preço dos 90 dias anteriores, **e** as duas condições abaixo:
  - **Histórico mínimo:** só alertar após N dias de coletas do produto (valor inicial sugerido: 7 dias; ajustável), evitando alertas falsos no início (*cold start*).
  - **Sem repetição:** não reenviar o alerta se o preço não ficou abaixo do último preço já alertado (tabela `alertas`).

## 5. Notificação
- **Status:** Aceita (a validar na implementação).
- **Decisão:** Mensagem instantânea via Bot do Telegram.
- **Razão:** Facilidade extrema de criação, integração via API HTTP simples e custo zero.
- **Segredos:** token e chat id em **GitHub Secrets** no Actions e em `.env` (fora do Git, via `.gitignore`) no ambiente local.

## 6. Preço rastreado
- **Status:** Aceita (decisão do autor, 2026-10-20).
- **Contexto:** A Kabum expõe três valores: `oldPrice` (preço "riscado" de marketing), `price` (preço cheio, parcelado/cartão) e `priceWithDiscount` (à vista no PIX, ~15% abaixo).
- **Decisão:** Guardar `preco_vista` e `preco_cheio` em cada coleta; ignorar `oldPrice`. O alerta é baseado em `preco_vista`.
- **Razão:** O à vista é o valor efetivamente pago e o mais comparável; guardar também o cheio custa uma coluna e evita refazer a coleta caso a regra mude.