# Architecture Decision Records (ADR)

## 1. Automation (Automação)
- **Decisão:** GitHub Actions (Cron Job a cada 12 horas).
- **Razão:** Viabilizar o projeto mantendo o custo zero, atendendo às restrições de infraestrutura.
- **Trade-off:** Limitação do tempo máximo de execução por job.

## 2. Coletor (Scraper Isolado)
- **Decisão:** Requisição HTTP pura (se estático) / Playwright (se dinâmico).
- **Razão:** Otimizar performance e consumo de recursos, alternando a estratégia conforme a necessidade técnica do site alvo.

## 3. Armazenamento (Banco de Dados)
- **Decisão:** SQLite.
- **Razão:** Armazenamento local estruturado, sem volatilidade, sem burocracia de servidores, com suporte a SQL nativo e custo zero.
- **Trade-off:** Não é ideal para escrita concorrente em altíssima escala (o que não é o nosso caso).

## 4. Processamento & Regra de Negócio
- **Lógica:** Consulta o menor valor histórico do produto nos últimos 90 dias.
- **Condição de Alerta:** Preço Atual <= Menor Preço dos últimos 90 dias $\rightarrow$ Disparar Alerta.

## 5. Notificação
- **Decisão:** Mensagem instantânea via Bot do Telegram.
- **Razão:** Facilidade extrema de criação, integração via API HTTP simples e custo zero.