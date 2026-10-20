# Software Requirements Specification (SRS)

## Business requirements:

- Objetivo: Comprar produtos pelo menor preço histórico do trimestre.
- Regra de valor: Identificar quando um produto atinge a menor faixa de preço dos últimos 90 dias para economizar dinheiro nas compras.
- Métricas de Sucesso: O usuário deve ser notificado a tempo antes que o preço volte a subir.

## Functional Requirements:

- Entrada de dados: O sistema deve permitir que o cliente cadastre uma lista de URLs de produtos.
- Coleta: O sistema deve extrair automaticamente o preço atual e o nome do produto a cada 12 horas.
- Armazenamento: O sistema deve armazenar o preço coletado junto com o timestamp.
- Processamento: O sistema deve consultar o histórico dos últimos 90 dias para calcular o menor valor registrado nesse período.
- Saída: Se o preço atual for menor ou igual ao menor preço dos últimos 90 dias, o sistema deve enviar uma mensagem ao usuário.

## Non-Functional Requirements:

- Tolerância a falhas: Caso o e-commerce rastreado bloqueie o IP temporariamente ou estiver fora do ar, o rastreador não pode quebrar o sistema inteiro; ele deve registrar o erro e tentar novamente mais tarde.
- Eficiência: O processo de varredura de todos os produtos cadastrados deve terminar em menos de 10 minutos pra não sobrecarregar recursos.
- Manutenibilidade: Como o layout dos e-commerces muda com frequência, o código de extração (scraping) deve estar isolado do resto do sistema para facilitar a manutenção quando um site quebrar a estrutura HTML.
- Segurança: Se você salvar credenciais ou chaves de API, elas não podem ficar expostas diretamente no código-fonte.,

## Constraints

- Orçamento $0: O projeto precisa rodar inteiramente usando ferramentas, servidores e APIs gratuitas.
- Prazo: Com poucas horas disponíveis por semana deve-se evitar usar arquiteturas complexas, como microsserviços ou Kubernetes.
- Limitações Externas: O e-commerce impõe bloqueios de taxa (rate limiting). Está restrito fazer no máximo X requisições por minuto para não ter o IP banido.