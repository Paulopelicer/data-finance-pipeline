---
name: pix-pipeline-generator
description: Skill para gerar, revisar e validar projetos completos de Engenharia de Dados do Pix com Python, PySpark, Apache Spark, Jupyter Notebook, camadas Bronze/Silver/Gold, dados públicos reais do Banco Central do Brasil, indicadores analíticos, estimativas hipotéticas de economia, gráficos, README, PRD funcional, PRD técnico, scripts de execução, scripts de validação e critérios de aceite. Use quando Codex precisar criar do zero ou revisar um pipeline de dados do Pix, projeto educacional de Engenharia de Dados com PySpark, arquitetura Data Lake em camadas, documentação técnica ou entrega completa com validação final.
---

# Pix Pipeline Generator Skill

## Purpose

Gerar ou revisar um projeto completo, didático e executável de Engenharia de Dados com PySpark para análise de dados públicos reais do Pix no Brasil.

## When to Use

Use esta skill quando o usuário pedir algo como:

- Criar um pipeline de Engenharia de Dados com PySpark para analisar dados do Pix.
- Gerar um projeto completo com Bronze, Silver, Gold, indicadores, gráficos e documentação para dados públicos do Pix.
- Criar um pipeline inspirado no projeto Pix usando dados públicos do Banco Central.
- Revisar ou validar um projeto Pix com PySpark, notebooks, PRDs e outputs finais.

## Expected Inputs

- Nome desejado do projeto ou autorização para usar `pix-data-pipeline-spark`.
- Diretório de destino.
- Preferência por execução local, notebook, terminal ou VSCode.
- Requisitos específicos de apresentação, se houver.
- Autorização explícita para instalar dependências, acessar rede, executar pipeline, commit ou push, quando aplicável.

## Expected Outputs

O projeto gerado deve conter:

- Estrutura de pastas profissional.
- Código Python em `src/`.
- Notebooks sequenciais em `notebooks/`.
- Scripts `run_pipeline.py`, `scripts/rebuild_pipeline.py`, `scripts/clean_outputs.py` e `scripts/validate_pipeline.py`.
- Camadas Bronze, Silver e Gold em Parquet.
- Indicadores mensais do Pix.
- Estimativas hipotéticas de economia.
- Gráficos finais em `reports/figures`.
- `README.md`, `docs/PRD_Functional.md`, `docs/PRD_Technical.md` e `data/input/README_input.md`.
- `requirements.txt` e `.gitignore`.
- Validação final executável.

## Project Architecture

Criar arquitetura local em camadas:

```text
Fonte pública Banco Central
        |
        v
Bronze: dados brutos em Parquet
        |
        v
Silver: dados limpos e padronizados em Parquet
        |
        v
Gold: indicadores e estimativas em Parquet
        |
        v
Reports: gráficos e arquivos analíticos pequenos
```

Leia `references/architecture.md` ao projetar ou revisar a arquitetura.

## Required Stack

Exigir, no mínimo:

- Python.
- PySpark.
- Apache Spark.
- Jupyter Notebook.
- pandas.
- matplotlib.
- requests.
- pathlib.
- Parquet.
- CSV apenas para entrada manual ou exportação pequena.
- Git e GitHub quando houver versionamento.
- VSCode e WSL Linux como ambiente local esperado.

## Required Folder Structure

Usar estrutura semelhante a:

```text
pix-data-pipeline-spark/
├── README.md
├── requirements.txt
├── .gitignore
├── run_pipeline.py
├── docs/
│   ├── PRD_Functional.md
│   └── PRD_Technical.md
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── spark_session.py
│   ├── data_source.py
│   ├── data_quality.py
│   └── utils.py
├── notebooks/
│   ├── 01_bronze_ingestion_pix.ipynb
│   ├── 02_silver_transform_pix.ipynb
│   ├── 03_gold_indicators_pix.ipynb
│   ├── 04_fee_savings_estimation_pix.ipynb
│   └── 05_data_viz_pix.ipynb
├── data/
│   ├── input/
│   │   └── README_input.md
│   ├── bronze/
│   ├── silver/
│   └── gold/
├── reports/
│   └── figures/
└── scripts/
    ├── clean_outputs.py
    ├── validate_pipeline.py
    └── rebuild_pipeline.py
```

Leia `references/pipeline_structure.md` para detalhes de cada diretório e script.

## Pipeline Stages

1. Ingestão Bronze: coletar dados públicos reais e salvar bruto em Parquet.
2. Transformação Silver: padronizar colunas, tipos, datas, nulos e filtros de qualidade.
3. Indicadores Gold: agregar por mês, calcular ticket médio e crescimento mensal.
4. Estimativas de economia: criar cenários hipotéticos com taxas de cartão e transferências.
5. Visualização: gerar gráficos finais com boa leitura para apresentação.

## Data Source Rules

- Usar dados públicos reais como execução padrão.
- Preferir fontes públicas do Banco Central do Brasil.
- Documentar a URL ou referência da fonte no README e nos PRDs.
- Implementar ingestão automática quando possível.
- Implementar fallback para CSV público manual em `data/input`.
- Proibir dados simulados como fallback padrão.
- Falhar com mensagem clara se não houver dado público real disponível.
- Registrar no console a origem usada e a quantidade de registros.

Leia `references/data_sources.md` antes de implementar ingestão.

## Bronze Layer Rules

- Salvar dados brutos em `data/bronze/pix_raw/`.
- Usar Parquet.
- Manter o dado próximo da origem.
- Evitar transformações complexas.
- Preservar rastreabilidade de fonte quando conveniente.

## Silver Layer Rules

- Ler Bronze.
- Normalizar nomes de colunas em snake_case.
- Remover acentos apenas de nomes técnicos.
- Converter data ou mês de referência.
- Criar `ano`, `mes` e `ano_mes`.
- Converter quantidade e valor para tipos numéricos.
- Remover registros totalmente nulos.
- Tratar nulos críticos com regra simples e documentada.
- Filtrar ou sinalizar valores negativos indevidos.
- Salvar em `data/silver/pix_clean/` em Parquet.

Leia `references/naming_standards.md` e `references/data_quality_rules.md` ao implementar Silver.

## Gold Layer Rules

Gerar tabela mensal com:

```text
ano_mes
quantidade_transacoes
valor_total
ticket_medio
crescimento_qtd_mes_anterior
crescimento_valor_mes_anterior
```

Usar as fórmulas:

```text
ticket_medio = valor_total / quantidade_transacoes
crescimento_percentual = ((valor_atual - valor_mes_anterior) / valor_mes_anterior) * 100
```

Tratar divisão por zero, nulos, ausência de mês anterior e inconsistência de tipos.

## Fee Savings Estimation Rules

A análise deve ser sempre apresentada como estimativa hipotética.

Texto obrigatório:

```text
A análise de economia potencial é baseada em cenários hipotéticos. Os dados públicos não identificam qual meio de pagamento cada transação Pix substituiu. Por isso, os valores calculados não representam economia real comprovada, mas sim uma simulação analítica para fins educacionais.
```

Leia `references/fee_savings_rules.md` antes de implementar cenários.

## Data Visualization Rules

Gerar os gráficos mínimos:

```text
01_pix_monthly_transactions.png
02_pix_monthly_value.png
03_pix_average_ticket.png
04_pix_estimated_card_fee_savings.png
05_pix_estimated_transfer_fee_savings.png
```

Cada gráfico deve ter título, eixo X, eixo Y, legenda quando aplicável, grid, fonte dos dados, escala legível, ausência de notação científica e observação de hipótese nos gráficos de economia.

Leia `references/visualization_standards.md` antes de alterar gráficos.

## Documentation Rules

Criar documentação com linguagem formal, técnica, objetiva e sem emojis:

- `README.md`.
- `docs/PRD_Functional.md`.
- `docs/PRD_Technical.md`.
- `data/input/README_input.md`.

O README deve explicar objetivo, contexto bancário, fonte, arquitetura, camadas, tecnologias, execução, validação, limpeza, indicadores, premissas, limitações, troubleshooting e melhorias futuras.

## PRD Rules

Criar PRD funcional e PRD técnico. Incluir diagramas Mermaid quando conveniente. Leia `references/prd_templates.md` para estrutura mínima e modelos.

## Data Quality Rules

Implementar validações de estrutura, schema, registros, nulos, tipos, ranges, valores negativos, divisão por zero, outputs e ausência de dados fictícios em execução padrão. Leia `references/data_quality_rules.md`.

## Validation Rules

Executar, no mínimo:

```bash
python -m compileall src scripts
python run_pipeline.py
python scripts/validate_pipeline.py
```

O validador deve verificar estrutura, notebooks, PRDs, camadas, registros, gráficos, ausência de hardcode, ausência de emojis, ausência de dados simulados como padrão, `.gitignore` e tratamento de `SPARK_HOME`.

Leia `references/validation_checklist.md` antes de finalizar.

## Git Rules

- Não fazer commit sem autorização explícita.
- Não fazer push sem autorização explícita.
- Criar `.gitignore` adequado.
- Recomendar versionar código, notebooks limpos, documentação e scripts.
- Recomendar ignorar outputs reproduzíveis, caches, `.crc`, `_SUCCESS`, `.pipeline_runs`, dados processados e figuras, salvo exigência explícita.

## Constraints

- Não usar emojis.
- Não hardcodar caminhos locais ou do Windows.
- Usar `pathlib.Path` para caminhos.
- Criar diretórios automaticamente.
- Usar PySpark nas transformações principais.
- Usar pandas apenas para ingestão auxiliar, amostras pequenas ou visualização.
- Não usar APIs pagas, credenciais, tokens ou dados privados.
- Não usar dados simulados como execução padrão.
- Tratar `SPARK_HOME` inválido de forma segura.
- Manter linguagem formal, técnica e objetiva.

## Acceptance Criteria

A entrega só deve ser considerada concluída quando:

1. Estrutura do projeto foi criada.
2. Código Python auxiliar existe.
3. Cinco notebooks sequenciais existem.
4. Dados públicos reais são usados como padrão.
5. Bronze, Silver e Gold usam Parquet.
6. Indicadores mensais são calculados.
7. Estimativas de economia são cenários hipotéticos.
8. Cinco gráficos são gerados.
9. README e PRDs existem.
10. Scripts de limpeza, execução e validação existem.
11. `.gitignore` é adequado.
12. `SPARK_HOME` inválido é tratado.
13. Não há emojis.
14. Não há hardcode de caminhos locais.
15. Validação final passa.
16. Commit e push não foram feitos sem autorização.

## Final Response Format

Responder ao usuário com:

```text
Projeto criado/revisado com sucesso.

Arquivos principais:
- README.md
- requirements.txt
- .gitignore
- run_pipeline.py
- src/...
- notebooks/...
- docs/...
- scripts/...

Validações executadas:
- python -m compileall src scripts
- python run_pipeline.py
- python scripts/validate_pipeline.py

Resultado:
- Bronze: <quantidade> registros
- Silver: <quantidade> registros
- Gold indicadores: <quantidade> registros
- Gráficos gerados: <lista>

Pontos de atenção:
- <quando houver>

Próximo passo recomendado:
- <commit/push somente se autorizado>
```
