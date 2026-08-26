# MCP CSV

Nesta versao, foi implementado o MCP CSV em dois modos: servidor MCP nativo via stdio para uso pelo Codex e CLI demonstravel para testes no terminal.

O MCP CSV permite consultar metricas, validar colunas, visualizar amostras e resumir os principais resultados do projeto sem alterar dados, notebooks, tabelas ou codigo do pipeline.

## Objetivo

O MCP CSV e uma interface local, read-only e segura para consultar arquivos CSV gerados em `reports/`.

Ele foi criado para demonstrar como um agente pode consumir os resultados analiticos do pipeline Pix por meio de ferramentas controladas, em vez de depender de leitura manual de arquivos.

## Modos Disponiveis

- MCP nativo via stdio: `python mcp/csv_mcp_server.py`
- MCP nativo explicito: `python mcp/csv_mcp_server.py --mcp-stdio`
- CLI demonstravel: `python mcp/csv_mcp_server.py --tool csv_get_metrics_summary`

## Ferramentas

- `csv_list_reports`: lista CSVs disponiveis em `reports/`.
- `csv_preview_file`: mostra amostra limitada de um CSV.
- `csv_describe_file`: retorna colunas, tipos e estatisticas basicas.
- `csv_validate_columns`: valida colunas esperadas.
- `csv_get_metrics_summary`: resume os principais CSVs de metricas.
- `csv_search_value`: busca termo textual nos CSVs.
- `csv_compare_metrics_files`: compara arquivos de metricas.

## Como Executar Pela CLI

```bash
python mcp/csv_mcp_server.py --list-tools
python mcp/csv_mcp_server.py --tool csv_list_reports
python mcp/csv_mcp_server.py --tool csv_get_metrics_summary
python mcp/csv_mcp_server.py --tool csv_preview_file --file reports/business_metrics_summary.csv
python mcp/csv_mcp_server.py --tool csv_describe_file --file reports/regression_metrics.csv
python mcp/csv_mcp_server.py --tool csv_validate_columns --file reports/regression_metrics.csv --columns metric,value
python mcp/csv_mcp_server.py --tool csv_search_value --query RMSE
python mcp/csv_mcp_server.py --tool csv_compare_metrics_files
```

## Como Usar No Codex

Consulte `mcp/CODEX_MCP_SETUP.md` para configurar o servidor no Codex.

Depois da configuracao, use pedidos em linguagem natural no chat, por exemplo:

```text
Use o MCP CSV para listar os reports disponiveis.
```

```text
Use o MCP CSV para resumir as metricas principais do projeto Pix.
```

```text
Use o MCP CSV para validar se reports/regression_metrics.csv possui as colunas metric e value.
```

## Seguranca

- Leitura apenas.
- Nao altera, remove ou cria dados.
- Bloqueia caminhos absolutos.
- Bloqueia `..`.
- Permite apenas arquivos `.csv`.
- Restringe leitura a pasta `reports/`.
- Limita quantidade de linhas retornadas em previews e buscas.

## Arquivos Consultados

- `reports/business_metrics_summary.csv`
- `reports/classification_metrics.csv`
- `reports/feature_correlation_matrix.csv`
- `reports/feature_selection_summary.csv`
- `reports/model_metrics_summary.csv`
- `reports/regression_metrics.csv`

## Validacao

```bash
python scripts/validate_mcp_csv.py
```

## Limitacoes

O MCP CSV foi mantido propositalmente simples e local. Ele nao implementa MCP Spark, MCP PowerBI, MCP DeltaLake ou MCP Brain nesta versao.

## Evolucoes Futuras

- MCP Spark para consultas diretas em Parquet e DataFrames.
- MCP PowerBI para integracao com dashboards.
- MCP DeltaLake para tabelas versionadas.
- MCP Brain para consulta estruturada da base documental.
