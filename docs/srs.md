# Software Requirements Specification (SRS)

Última revisão: 2026-10-20

## Business requirements

- **Objetivo:** Comprar produtos pelo menor preço histórico do trimestre.
- **Regra de valor:** Identificar quando um produto atinge o menor preço (à vista) dos últimos 90 dias, para economizar dinheiro nas compras.
- **Métricas de sucesso:**
  - O alerta deve ser enviado em até 12 horas após a queda de preço (limite dado pela frequência de coleta).
  - O sistema deve rodar sem intervenção manual, e falhas persistentes devem ser notificadas.

## Functional Requirements

- **Entrada de dados:** O sistema deve permitir cadastrar uma lista de URLs de produtos, mantida em um arquivo versionado no repositório.
- **Coleta:** O sistema deve extrair automaticamente o nome do produto e os preços **à vista** (`preco_vista`) e **cheio** (`preco_cheio`) a cada 12 horas.
- **Armazenamento:** O sistema deve armazenar os preços coletados junto com o timestamp (UTC), em centavos.
- **Processamento:** O sistema deve consultar o histórico dos últimos 90 dias para calcular o menor `preco_vista` registrado nesse período, desconsiderando a coleta atual.
- **Saída (alerta):** Se o preço à vista atual for menor ou igual ao menor dos 90 dias anteriores, o sistema deve enviar uma mensagem ao usuário, respeitando duas regras:
  - **Histórico mínimo:** só alertar após N dias de coletas do produto (valor inicial sugerido: 7 dias).
  - **Sem repetição:** não reenviar alerta enquanto o preço não ficar abaixo do último preço alertado.
- **Notificação de falhas:** O sistema deve avisar o usuário quando um produto falhar em coletas consecutivas (valor inicial sugerido: 3 execuções).

## Non-Functional Requirements

- **Tolerância a falhas:** Caso o e-commerce bloqueie o IP temporariamente ou esteja fora do ar, o rastreador não pode quebrar o sistema inteiro: deve registrar o erro, tentar novamente (até 3 tentativas com espera crescente) e seguir para o próximo produto. Preços ausentes ou inválidos nunca são gravados no histórico.
- **Eficiência:** O processo de varredura de todos os produtos cadastrados deve terminar em menos de 10 minutos, para não sobrecarregar recursos.
- **Manutenibilidade:** Como o layout dos e-commerces muda com frequência, o código de extração (scraping) deve estar isolado do resto do sistema, para facilitar a manutenção quando um site mudar sua estrutura.
- **Testabilidade:** Os extratores devem ser testáveis offline, usando páginas HTML salvas (fixtures).
- **Segurança:** Credenciais e chaves de API não podem ficar expostas no código-fonte. Devem ser armazenadas em GitHub Secrets (nuvem) e `.env` ignorado pelo Git (local).
- **Reprodutibilidade:** As dependências devem ter versões fixadas e o ambiente local deve usar a mesma versão do Python que o workflow.

## Constraints

- **Orçamento $0:** O projeto precisa rodar inteiramente usando ferramentas, servidores e APIs gratuitas.
- **Prazo:** Com poucas horas disponíveis por semana, deve-se evitar arquiteturas complexas, como microsserviços ou Kubernetes.
- **Limitações externas:** O e-commerce impõe bloqueios de taxa (rate limiting). Valor inicial adotado: no máximo 1 requisição a cada 3 segundos por loja, com variação aleatória, ajustável conforme os testes.
- **Execução em nuvem efêmera:** O ambiente de execução (GitHub Actions) não guarda estado entre execuções; a persistência dos dados é tratada no ADR 3.