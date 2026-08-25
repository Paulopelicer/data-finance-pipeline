# Estrutura do Projeto

## Estrutura Esperada

```text
pix-data-pipeline-spark/
├── README.md
├── requirements.txt
├── .gitignore
├── run_pipeline.py
├── docs/
├── src/
├── notebooks/
├── data/
├── reports/
└── scripts/
```

## Diretórios

- `src/`: módulos reutilizáveis de configuração, Spark, fonte, qualidade e utilidades.
- `notebooks/`: execução didática sequencial do pipeline.
- `data/input/`: fallback manual para CSV público real.
- `data/bronze/`: dados brutos em Parquet.
- `data/silver/`: dados tratados em Parquet.
- `data/gold/`: indicadores e estimativas em Parquet.
- `reports/figures/`: gráficos finais.
- `docs/`: PRDs e documentação complementar.
- `scripts/`: limpeza, execução e validação.

## Notebooks

Usar nomes sequenciais:

```text
01_bronze_ingestion_pix.ipynb
02_silver_transform_pix.ipynb
03_gold_indicators_pix.ipynb
04_fee_savings_estimation_pix.ipynb
05_data_viz_pix.ipynb
```

## Scripts

- `run_pipeline.py`: ponto de entrada principal.
- `scripts/rebuild_pipeline.py`: executa notebooks em ordem e valida outputs.
- `scripts/clean_outputs.py`: remove outputs e artefatos temporários.
- `scripts/validate_pipeline.py`: valida estrutura, dados, gráficos e documentação.
