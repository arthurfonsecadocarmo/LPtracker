# Product Backlog - LPtracker

## Épico 1: Fundamentação e Setup

- **US-01: Configuração do Repositório e Documentação**
    - *História:* Como desenvolvedor, quero estruturar as pastas do projeto e documentar os requisitos e a arquitetura para garantir manutenibilidade e clareza.
    - *Definition of Done:*
        - Pastas `src/`, `docs/`, `data/` criadas.
        - Arquivos `docs/srs.md` e `docs/adr.md` preenchidos e commitados.
        - Arquivo `README.md` criado na raiz.
- **US-02: Configuração do Ambiente de Desenvolvimento**
    - *História:* Como desenvolvedor, quero configurar um ambiente virtual Python isolado para gerenciar as dependências do projeto.
    - *Definition of Done:*
        - Ambiente virtual (`venv`) ativado.
        - Arquivo `requirements.txt` gerado com as bibliotecas iniciais (`requests`, `beautifulsoup4`).

---

## Épico 2: Coleta de Dados (Scraping)

- **US-03: Prototipagem do Coletor Estático (BaseScraper)**
    - *História:* Como sistema, quero coletar o preço atual de um produto via requisição HTTP para otimizar a velocidade de varredura.
    - *Critérios de Aceite:*
        - Classe `BaseScraper` estruturada.
        - Subclasse implementada para uma loja de teste (ex: Mercado Livre).
        - Script de teste retornando o valor numérico (float) do preço no terminal.
- **US-04: Tratamento de Exceções no Scraping**
    - *História:* Como sistema, quero registrar falhas de conexão ou bloqueios de IP sem quebrar a execução geral, garantindo tolerância a falhas.
    - *Definition of Done:*
        - Blocos `try-except` encapsulando as requisições.
        - Log de erro impresso no console caso o elemento HTML não seja encontrado.

---

## Épico 3: Persistência de Dados

- **US-05: Modelagem e Criação do Banco SQLite**
    - *História:* Como sistema, quero criar um banco de dados local estruturado para armazenar o histórico temporal dos produtos.
    - *Definition of Done:*
        - Script de inicialização criando as tabelas `produtos` e `historico_precos` no arquivo `data/tracker.db`.
- **US-06: Persistência Automática da Coleta**
    - *História:* Como sistema, quero salvar no banco o preço coletado junto com o timestamp da execução.
    - *Definition of Done:*
        - Cada execução bem-sucedida do scraper insere um novo registro na tabela `historico_precos`.

---

## Épico 4: Regra de Negócio & Análise Temporal

- **US-07: Consulta do Menor Preço Histórico (90 Dias)**
    - *História:* Como sistema, quero consultar os registros dos últimos 90 dias para identificar o menor valor já cobrado pelo produto.
    - *Definition of Done:*
        - Query SQL ou função Python filtrando `data_coleta >= NOW() - 90 dias` e retornando o `MIN(preco)`.

---

## Épico 5: Notificações & Automação

- **US-08: Integração com Bot do Telegram**
    - *História:* Como usuário, quero receber alertas instantâneos no Telegram sempre que um produto atingir a baixa histórica.
    - *Definition of Done:*
        - Bot criado via BotFather, token configurado em variáveis de ambiente (`.env`).
        - Função de disparo de mensagem HTTP funcionando via script.
- **US-09: Automação via GitHub Actions**
    - *História:* Como desenvolvedor, quero que o script rode automaticamente a cada 12 horas na nuvem de forma gratuita.
    - *Definition of Done:*
        - Arquivo `.github/workflows/scraper.yml` configurado com trigger de `cron`.