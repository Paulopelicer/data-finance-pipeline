# Pix Pipeline Paulo HP

## Descricao

Este projeto implementa um pipeline educacional de Engenharia de Dados com PySpark para ingestao, tratamento, agregacao e visualizacao de dados publicos reais do Pix no Brasil.

O pipeline simula um fluxo analitico que poderia apoiar areas de meios de pagamento, canais digitais, inteligencia comercial, planejamento estrategico e BI de uma instituicao financeira. Embora tenha inspiracao no cotidiano bancario, utiliza exclusivamente dados publicos e nao contem informacoes internas, sensiveis ou privadas de qualquer instituicao.

## Objetivo

O objetivo e demonstrar, de forma simples e executavel, conceitos iniciais de Engenharia de Dados:

1. Ingestao de fonte publica real.
2. Organizacao em camadas Bronze, Silver e Gold.
3. Transformacoes com PySpark.
4. Criacao de indicadores mensais.
5. Estimativa hipotetica de economia potencial.
6. Geracao de graficos finais para apresentacao.

## Fonte Publica dos Dados

A execucao padrao consome dados reais da API OData de dados abertos do Banco Central do Brasil:

```text
https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/EstatisticasTransacoesPix(Database=@Database)?@Database='202401'&$top=50000&$format=json
```

A fonte retorna estatisticas de transacoes Pix com campos como `AnoMes`, `VALOR` e `QUANTIDADE`. Caso o acesso automatico falhe, o projeto aceita um arquivo CSV publico baixado manualmente e colocado em `data/input`. Esse fallback nao usa dados ficticios.

## Arquitetura do Pipeline

```text
Fonte publica Banco Central
        |
        v
Camada Bronze: dados brutos em Parquet
        |
        v
Camada Silver: dados limpos e padronizados em Parquet
        |
        v
Camada Gold: indicadores e estimativas em Parquet
        |
        v
Reports: graficos em PNG
```

## Camadas de Dados

A camada Bronze armazena os dados brutos, preservando a estrutura de origem tanto quanto possivel.

A camada Silver padroniza nomes de colunas, tipos numericos, referencia mensal e filtros simples de qualidade.

A camada Gold cria tabelas agregadas e prontas para consumo analitico, incluindo indicadores mensais e cenarios de economia potencial estimada.

## Estrutura de Pastas

```text
pix_pipeline_paulo_hp/
├── README.md
├── requirements.txt
├── .gitignore
├── run_pipeline.py
├── docs/
│   ├── PRD_Functional.md
│   └── PRD_Technical.md
├── src/
│   ├── config.py
│   ├── spark_session.py
│   ├── data_source.py
│   ├── data_quality.py
│   └── utils.py
├── scripts/
│   ├── clean_outputs.py
│   ├── rebuild_pipeline.py
│   ├── validate_pipeline.py
│   └── presentation_demo.py
├── notebooks/
│   ├── 01_bronze_ingestion_pix.ipynb
│   ├── 02_silver_transform_pix.ipynb
│   ├── 03_gold_indicators_pix.ipynb
│   ├── 04_fee_savings_estimation_pix.ipynb
│   └── 05_data_viz_pix.ipynb
├── data/
│   ├── input/
│   ├── bronze/
│   ├── silver/
│   └── gold/
└── reports/
    └── figures/
```

## Notebooks e Scripts

`01_bronze_ingestion_pix.ipynb` coleta dados publicos reais do Banco Central ou carrega CSV publico manual, valida os registros e salva a camada Bronze.

`02_silver_transform_pix.ipynb` le a camada Bronze, padroniza colunas, tipos, datas e salva a camada Silver.

`03_gold_indicators_pix.ipynb` le a camada Silver, agrega os dados por mes e calcula indicadores analiticos.

`04_fee_savings_estimation_pix.ipynb` calcula cenarios hipoteticos de economia potencial com taxas de cartao e tarifas de transferencias.

`05_data_viz_pix.ipynb` gera graficos finais a partir das tabelas Gold.

`run_pipeline.py` executa todos os notebooks em ordem, limpa outputs anteriores, trata `SPARK_HOME` invalido e valida os outputs obrigatorios.

`scripts/clean_outputs.py` remove dados gerados, figuras, caches e artefatos de execucao.

`scripts/validate_pipeline.py` valida estrutura, notebooks, outputs, ausencia de caminhos absolutos do Windows e ausencia de emojis nos arquivos principais.

## Tecnologias Utilizadas

- Python
- PySpark
- pandas
- requests
- matplotlib
- Jupyter Notebook
- Parquet
- WSL Linux

## Instalacao

No terminal do VSCode, a partir da raiz do projeto:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Opcionalmente, registre o kernel para uso nos notebooks:

```bash
python -m ipykernel install --user --name pix-data-pipeline-spark --display-name "Python (pix-data-pipeline-spark)"
```

## Execucao do Pipeline

Para executar o projeto do inicio ao fim:

```bash
source .venv/bin/activate
python run_pipeline.py
```

O comando limpa outputs anteriores, executa os notebooks em sequencia e gera novamente Bronze, Silver, Gold e graficos.

## Execucao dos Notebooks

Os notebooks podem ser executados individualmente no VSCode ou Jupyter, sempre na ordem:

1. `01_bronze_ingestion_pix.ipynb`
2. `02_silver_transform_pix.ipynb`
3. `03_gold_indicators_pix.ipynb`
4. `04_fee_savings_estimation_pix.ipynb`
5. `05_data_viz_pix.ipynb`

Para abrir Jupyter pelo terminal:

```bash
jupyter notebook
```

## Limpeza e Regeneracao de Outputs

Para limpar dados gerados e artefatos de execucao:

```bash
python scripts/clean_outputs.py
```

Para regenerar tudo:

```bash
python run_pipeline.py
```

## Indicadores Gerados

A tabela `data/gold/pix_monthly_indicators` contem:

- `ano_mes`
- `quantidade_transacoes`
- `valor_total`
- `ticket_medio`
- `crescimento_qtd_mes_anterior`
- `crescimento_valor_mes_anterior`

O ticket medio e calculado por:

```text
ticket_medio = valor_total / quantidade_transacoes
```

O crescimento mensal e calculado por:

```text
crescimento_percentual = ((valor_atual - valor_mes_anterior) / valor_mes_anterior) * 100
```

## Estimativa de Economia

A analise de economia potencial e baseada em cenarios hipoteticos. Os dados publicos nao identificam qual meio de pagamento cada transacao Pix substituiu. Por isso, os valores calculados nao representam economia real comprovada, mas sim uma simulacao analitica para fins educacionais.

Para cartao, sao utilizadas taxas didaticas de referencia:

- MDR debito: 1,08%.
- MDR credito: 2,26%.

Para transferencias tradicionais, sao utilizadas tarifas hipoteticas:

- tarifa baixa: R$ 5,00.
- tarifa media: R$ 10,00.
- tarifa alta: R$ 15,00.

As premissas podem variar por instituicao, adquirente, bandeira, segmento, contrato e periodo. Portanto, os resultados nao devem ser interpretados como economia real comprovada.

## Outputs Finais

O pipeline gera:

```text
data/bronze/pix_raw/
data/silver/pix_clean/
data/gold/pix_monthly_indicators/
data/gold/pix_fee_savings_estimation/
data/gold/pix_transfer_savings_estimation/
reports/figures/01_pix_monthly_transactions.png
reports/figures/02_pix_monthly_value.png
reports/figures/03_pix_average_ticket.png
reports/figures/04_pix_estimated_card_fee_savings.png
reports/figures/05_pix_estimated_transfer_fee_savings.png
```

## Validacao

Depois da execucao, valide o projeto com:

```bash
python -m compileall src scripts
python scripts/validate_pipeline.py
```

## Troubleshooting em WSL e PySpark

Se `SPARK_HOME` estiver configurado para um caminho inexistente, o projeto remove essa variavel apenas durante a execucao para permitir que o PySpark instalado no ambiente virtual seja usado corretamente.

Se o download automatico falhar, baixe um CSV publico do Banco Central contendo `AnoMes`, `VALOR` e `QUANTIDADE`, coloque em `data/input` e execute novamente.

Se o Jupyter nao abrir automaticamente no navegador pelo WSL, copie a URL exibida no terminal e abra no navegador do Windows.

## Instrucoes para Apresentacao

Para demonstrar o projeto, execute:

```bash
source .venv/bin/activate
python run_pipeline.py
python scripts/validate_pipeline.py
python scripts/presentation_demo.py
```

Em seguida, apresente a jornada Bronze, Silver, Gold, os indicadores mensais, os cenarios hipoteticos de economia e os graficos em `reports/figures`.

## Limitacoes

- A granularidade depende dos dados retornados pela API publica.
- O pipeline nao identifica qual meio de pagamento foi substituido por cada transacao Pix.
- As estimativas de economia sao hipoteticas e educacionais.
- A execucao depende de conectividade com a fonte publica ou de CSV publico manual em `data/input`.

## Aviso Educacional

Este projeto tem finalidade exclusivamente educacional.

O pipeline foi construido para demonstrar conceitos iniciais de Engenharia de Dados com PySpark, incluindo ingestao, camadas Bronze, Silver e Gold, transformacao, agregacao, geracao de indicadores e visualizacao.

As estimativas de economia sao baseadas em cenarios hipoteticos e nao representam valores reais comprovados. Os resultados nao devem ser utilizados como analise financeira oficial, recomendacao comercial ou afirmacao institucional.

## Melhorias Futuras

1. Comparar Pix com series publicas de cartao de debito e credito.
2. Adicionar analise por municipio e UF, quando disponivel na fonte.
3. Criar ranking de regioes ou segmentos com maior volume financeiro.
4. Criar dashboard em Power BI, Streamlit ou Dash.
5. Automatizar o pipeline com Apache Airflow.
6. Salvar os dados em Delta Lake.
7. Criar validacoes de qualidade de dados mais completas.
8. Criar testes automatizados.
9. Criar execucao via Docker.
10. Publicar o projeto como portfolio tecnico.


## Analytics e Machine Learning Educacional

O projeto foi ampliado com EDA, feature engineering, feature selection, regressão, classificação e consolidação de métricas. Essas etapas têm finalidade educacional e não devem ser usadas para previsão financeira oficial.

Novos notebooks:

```text
00_run_all.ipynb
03_eda_pix.ipynb
06_feature_engineering_pix.ipynb
07_feature_selection_pix.ipynb
08_prediction_regression_pix.ipynb
09_prediction_classification_pix.ipynb
10_metrics_pix.ipynb
```

Novos comandos:

```bash
python scripts/test_few.py --rows 500
python run_pipeline.py
python scripts/validate_pipeline.py
pytest
python scripts/validate_agents_skills.py
```

## MCP e Brain

O projeto possui um MCP CSV implementado em dois modos: nativo via stdio para uso pelo Codex e CLI para demonstracao no terminal.

Brain nao foi implementado como ferramenta externa. A pasta `docs/knowledge_base/` atua como base de conhecimento documental inicial do projeto.

## Agentes e Skills

A pasta `agents_skills/` contem skills para apresentacao e documentacao. Elas nao fazem parte da execucao obrigatoria do pipeline. As skills agnosticas podem ser reutilizadas em outros projetos de dados; a skill `pix-pipeline-generator` e especifica do caso Pix.

## MCP CSV

Nesta versao, o projeto implementa somente o MCP CSV. Ele e uma interface local, read-only, demonstravel por CLI e conectavel ao Codex como servidor MCP nativo via stdio.

O MCP CSV permite listar reports, visualizar amostras, descrever arquivos, validar colunas, buscar termos e resumir metricas sem alterar dados, notebooks, tabelas ou codigo do pipeline.

Comandos principais:

```bash
python mcp/csv_mcp_server.py --list-tools
python mcp/csv_mcp_server.py --tool csv_list_reports
python mcp/csv_mcp_server.py --tool csv_get_metrics_summary
python scripts/validate_mcp_csv.py
```

Configuracao para uso no Codex:

```text
mcp/CODEX_MCP_SETUP.md
```

Depois de configurado, o usuario pode interagir no chat do Codex em linguagem natural, por exemplo: "Use o MCP CSV para resumir as metricas principais do projeto Pix".

Nao foram implementados MCP Spark, MCP PowerBI, MCP DeltaLake ou MCP Brain nesta versao. Esses itens permanecem como evolucoes futuras para evitar complexidade desnecessaria antes da apresentacao.

## Brain Documental

O projeto possui uma base documental inicial em `docs/knowledge_base/`, classificada como Brain documental em Markdown. Ela organiza regras de negocio, decisoes tecnicas, dicionario de dados, catalogo de fontes e aprendizados. Nao ha MCP Brain, banco vetorial, SQLite, Obsidian ou Graphify implementado nesta versao.

## Demonstracao Para O Gestor

1. Executar `python run_pipeline.py` para demonstrar o pipeline completo.
2. Executar `python scripts/validate_pipeline.py` para comprovar estrutura e outputs.
3. Executar `python mcp/csv_mcp_server.py --list-tools` para demonstrar o MCP CSV.
4. Executar `python mcp/csv_mcp_server.py --tool csv_get_metrics_summary` para consultar metricas analiticas.
5. Executar `python scripts/validate_agents_skills.py` para validar agents/skills.
6. Apresentar `docs/requirements_traceability_matrix.md` como matriz de aderencia.
