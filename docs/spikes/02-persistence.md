# Spike 02 — Persistência do SQLite entre execuções do GitHub Actions

**Data:** 2026-10-21 (madrugada, horário de Salvador; 03:54 UTC)
**Código:** `src/spike_persistence.py` e `.github/workflows/spike-persistencia.yml`

## Pergunta
O banco SQLite, commitado de volta no repositório ao fim de cada execução, sobrevive entre execuções do runner efêmero do GitHub Actions? (ADR 3)

## Método
Script que cria (se não existir) a tabela `execucoes` em `data/spike.db`, insere uma linha com o horário UTC e imprime o total de linhas. O workflow, disparado manualmente, roda o script e em seguida faz `git add`, `git commit` e `git push` do arquivo como `github-actions[bot]`.

Configuração relevante: `permissions: contents: write` e `concurrency` com grupo próprio, sem cancelar execuções em andamento.

## Resultado
- 1ª execução: `Linhas na tabela execucoes: 1`.
- 2ª execução: `Linhas na tabela execucoes: 2`. O banco veio do repositório (via `checkout`), ganhou uma linha e foi salvo de volta.
- O log da 2ª execução mostra `GITHUB_TOKEN Permissions: Contents: write`, o commit `1334d60 chore: atualizar spike.db` e o push `83bab34..1334d60 main -> main`.
- Ambiente: Ubuntu 24.04, Python 3.14.8 (o `python-version: "3.14"` resolve para o último patch disponível).

## Conclusão
A persistência via commit no repositório funciona. O ADR 3 pode passar de **Proposta** para **Aceita**.

## Riscos e pendências
- O arquivo binário cresce a cada commit e o Git guarda todas as versões. Reavaliar se o repositório ficar pesado (alternativa: exportar o histórico para CSV/JSON ou usar um banco hospedado).
- Se o runner e o PC alterarem o banco ao mesmo tempo, haverá divergência: fazer `git pull` antes de trabalhar localmente e não commitar o `tracker.db` pelo PC.
- A versão do Python varia no patch (3.14.7 → 3.14.8); fixar o patch se isso causar diferenças.
- Este spike usa `data/spike.db`. O banco real (`data/tracker.db`) será outro arquivo.