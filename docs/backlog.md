# Product Backlog - LPtracker

Última revisão: 2026-10-21

**Legenda:** ✅ concluído · 🔄 em andamento · ⬜ a fazer

## Como ler este backlog

O trabalho está organizado em **fatias ponta a ponta** (e não em camadas): cada fatia entrega algo que já funciona sozinho. As histórias mantêm os IDs originais (US-01 a US-09); as novas começam em US-10. Os spikes (testes de risco) têm IDs próprios (SP-xx).

## Definition of Done global
Uma história só está pronta quando:
- o código está em `src/` e roda no GitHub Actions (quando aplicável), não só no PC;
- não há segredos no código (usar `.env` local e GitHub Secrets na nuvem);
- a documentação afetada (README, SRS, ADR) foi atualizada;
- o commit tem mensagem que explica o porquê.

## Visão geral das fatias

| Fatia | Objetivo | Histórias | Status |
|---|---|---|---|
| 0 | Fundação e validação dos riscos | US-01, US-02, SP-01, SP-02 | 🔄 |
| 1 | Coleta contínua de 1 produto, sem alerta (o histórico já começa a acumular) | US-02, US-03, US-05, US-06, US-10, US-09 | ⬜ |
| 2 | Confiabilidade da coleta | US-04, US-12, US-14 | ⬜ |
| 3 | Alerta de baixa histórica | US-07, US-15, US-08 | ⬜ |
| 4 | Robustez e vitrine | US-13, US-16, US-17, US-18, US-19 | ⬜ |

---

## Fatia 0 — Fundação e validação dos riscos

- **US-01: Configuração do Repositório e Documentação** 🔄
    - *História:* Como desenvolvedor, quero estruturar as pastas do projeto e documentar os requisitos e a arquitetura para garantir manutenibilidade e clareza.
    - *Definition of Done:*
        - Pastas `src/`, `docs/`, `data/` criadas.
        - `docs/srs.md`, `docs/adr.md` e `docs/backlog.md` atualizados e commitados.
        - `README.md` criado na raiz (o que é o projeto, como rodar, status atual).
- **SP-01: Spike — leitura de preço da Kabum no Actions** ✅
    - Resultado em `docs/spikes/01-kabum.md`.
- **SP-02: Spike — persistência do SQLite via commit** ✅
    - Resultado em `docs/spikes/02-persistencia.md`.

---

## Fatia 1 — Coleta contínua de 1 produto (sem alerta)

*Meta da fatia:* depois de 2 dias, o repositório contém um `data/tracker.db` com pelo menos 4 registros de preço, commitados pelo robô, sem nenhuma intervenção manual.

- **US-02: Configuração do Ambiente de Desenvolvimento** 🔄
    - *História:* Como desenvolvedor, quero um ambiente virtual Python isolado para gerenciar as dependências do projeto.
    - *Definition of Done:*
        - Ambiente virtual (`venv`) ativado e fora do Git (`.gitignore`).
        - `requirements.txt` com `requests` e `beautifulsoup4` em versões fixadas.
        - Versão do Python registrada no README e igual à usada no workflow.
- **US-03: Coletor da Kabum (BaseScraper + KabumScraper)** ⬜
    - *História:* Como sistema, quero coletar o nome e os preços de um produto via requisição HTTP para alimentar o histórico.
    - *Critérios de Aceite:*
        - Classe `BaseScraper` com o contrato comum (receber uma URL, devolver nome, `preco_vista` e `preco_cheio`).
        - `KabumScraper` lê o `__NEXT_DATA__` (campos `priceWithDiscount` e `price`) e usa o JSON-LD como reserva.
        - Preços convertidos para **centavos (inteiro)**.
        - Script de teste imprime o resultado no terminal.
- **US-05: Modelagem e Criação do Banco SQLite** ⬜
    - *História:* Como sistema, quero um banco local estruturado para armazenar o histórico temporal dos produtos.
    - *Definition of Done:*
        - Script de inicialização cria, em `data/tracker.db`, as tabelas:
            - `produtos(id, url, nome, loja, ativo)`
            - `historico_precos(id, produto_id, preco_vista_centavos, preco_cheio_centavos, coletado_em)`
            - `alertas(id, produto_id, preco_vista_centavos, enviado_em)`
            - `falhas(id, produto_id, ocorrido_em, motivo)`
        - Horários em UTC (ISO 8601); índice em `(produto_id, coletado_em)`.
        - O script pode rodar várias vezes sem apagar dados.
- **US-10: Lista de produtos acompanhados** ⬜
    - *História:* Como usuário, quero cadastrar as URLs que serão acompanhadas, para não precisar mexer no código.
    - *Definition of Done:*
        - Arquivo versionado (ex.: `produtos.yaml`) com a lista; começa com **1 produto** (RX 7600 ASRock, Kabum).
        - O sistema lê a lista e sincroniza a tabela `produtos`.
- **US-06: Persistência Automática da Coleta** ⬜
    - *História:* Como sistema, quero salvar no banco os preços coletados junto com o timestamp da execução.
    - *Definition of Done:*
        - Cada execução bem-sucedida insere um registro em `historico_precos`.
        - Preços ausentes ou inválidos não são gravados.
- **US-09: Automação via GitHub Actions** ⬜
    - *História:* Como desenvolvedor, quero que o script rode automaticamente a cada 12 horas na nuvem, de graça, e que o banco persista entre execuções.
    - *Definition of Done:*
        - `.github/workflows/scraper.yml` com trigger de `cron` (a cada 12 horas) e também `workflow_dispatch`.
        - `permissions: contents: write` e `concurrency` configurados.
        - Ao fim da execução, o workflow faz commit e push de `data/tracker.db` como `github-actions[bot]`.
        - `runs-on: ubuntu-24.04` fixado.

---

## Fatia 2 — Confiabilidade da coleta

- **US-04: Tratamento de Exceções no Scraping** ⬜
    - *História:* Como sistema, quero registrar falhas de conexão ou bloqueios sem quebrar a execução geral, garantindo tolerância a falhas.
    - *Definition of Done:*
        - `try-except` encapsulando as requisições, com `timeout`.
        - Falhas registradas na tabela `falhas` e no log do Actions.
        - Erro claro quando um campo esperado do HTML/JSON não é encontrado.
- **US-12: Retry com espera crescente** ⬜
    - *História:* Como sistema, quero tentar novamente quando uma requisição falhar, para não perder coletas por instabilidades momentâneas.
    - *Definition of Done:*
        - Até 3 tentativas, com espera crescente entre elas.
        - Após a última tentativa, a falha é registrada e o sistema segue para o próximo produto.
- **US-14: Testes do extrator com HTML salvo** ⬜
    - *História:* Como desenvolvedor, quero testar o extrator sem depender da internet, para detectar rápido quando o layout do site mudar.
    - *Definition of Done:*
        - Um HTML real da Kabum salvo em `tests/fixtures/`.
        - Testes com `pytest` verificam nome e preços extraídos, e o comportamento quando o campo não existe.

---

## Fatia 3 — Alerta de baixa histórica

- **US-07: Consulta do Menor Preço Histórico (90 Dias)** ⬜
    - *História:* Como sistema, quero consultar os registros dos 90 dias anteriores para identificar o menor preço à vista já cobrado.
    - *Definition of Done:*
        - Função/consulta SQL filtrando `coletado_em` nos últimos 90 dias, **excluindo a coleta atual**, e retornando o `MIN(preco_vista_centavos)`.
        - Testes cobrindo: sem histórico, histórico curto e histórico completo.
- **US-15: Regra de alerta (histórico mínimo e sem repetição)** ⬜
    - *História:* Como usuário, quero ser avisado só quando fizer sentido, sem alertas falsos no início e sem mensagens repetidas.
    - *Definition of Done:*
        - Só alerta se o produto tiver pelo menos N dias de coletas (valor inicial: 7, configurável).
        - Alerta quando o preço à vista atual é menor ou igual ao menor dos 90 dias anteriores.
        - Não reenvia se o preço não ficou abaixo do último preço alertado (tabela `alertas`).
        - Testes cobrindo esses três cenários.
- **US-08: Integração com Bot do Telegram** ⬜
    - *História:* Como usuário, quero receber alertas instantâneos no Telegram sempre que um produto atingir a baixa histórica.
    - *Definition of Done:*
        - Bot criado via BotFather; token e chat id em `.env` (local, fora do Git) e em **GitHub Secrets** (nuvem).
        - Função de envio via HTTP funcionando, com mensagem contendo nome, preço à vista e link do produto.
        - Teste de ponta a ponta: mensagem recebida no Telegram a partir do Actions.

---

## Fatia 4 — Robustez e vitrine

- **US-13: Alerta de falha persistente** ⬜
    - *História:* Como usuário, quero ser avisado quando a coleta de um produto falhar várias vezes seguidas, para saber que o scraper quebrou.
    - *Definition of Done:*
        - Mensagem no Telegram após N execuções consecutivas com falha (valor inicial: 3).
        - Sem repetição da mensagem a cada execução.
- **US-16: Limite de requisições (rate limiting)** ⬜
    - *História:* Como sistema, quero espaçar as requisições para não ser bloqueado.
    - *Definition of Done:*
        - Pausa de ~3 segundos, com variação aleatória, entre requisições à mesma loja (valor configurável).
        - Necessário principalmente quando houver mais de um produto.
- **US-17: README e documentação final** ⬜
    - *História:* Como visitante do repositório, quero entender o projeto e rodá-lo.
    - *Definition of Done:*
        - README com objetivo, arquitetura resumida, como configurar segredos, como rodar localmente e decisões principais (links para ADR e spikes).
- **US-18: Manutenção e higiene do projeto** ⬜
    - *História:* Como desenvolvedor, quero manter o projeto atualizado e organizado.
    - *Definition of Done:*
        - Actions (`checkout`, `setup-python`) atualizadas para versões sem aviso de depreciação.
        - Arquivos dos spikes organizados ou removidos (o relatório em `docs/spikes/` permanece).
        - Verificado que o workflow agendado continua ativo.
- **US-19 (opcional): Gráfico do histórico de preços** ⬜
    - *História:* Como usuário, quero ver a evolução do preço ao longo do tempo.
    - *Definition of Done:*
        - Gráfico gerado a partir do `tracker.db` (ex.: imagem ou página estática no GitHub Pages).

---

## Riscos em observação
- **Bloqueio intermitente da loja:** a leitura funcionou no Actions, mas pode falhar em outros horários. Cobertura: US-04, US-12 e US-13.
- **Mudança na estrutura interna do site:** cobertura: US-14 (testes) e US-13 (alerta de falha).
- **Crescimento do arquivo do banco no Git:** reavaliar se o repositório ficar pesado (ADR 3).