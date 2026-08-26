# stf_pss_ms_data_finance_pipeline

Pipeline financeiro consolidado com dois modulos independentes:

- B3: ingestao de cotacoes, tratamento OHLCV, metricas Gold e relatorio PDF.
- Pix: ingestao de dados publicos do Banco Central, indicadores mensais, estimativas hipoteticas, analytics e graficos.

O projeto segue os padroes Stefanini PSS definidos em `project_patteners.md`, usando backend, middleware, testes, documentacao, infraestrutura e miscelanea. Nao existe `c_frontend/` porque os projetos originais nao possuem frontend.

## Arquitetura

```text
Fontes publicas/autorizadas
        |
        v
a_backend/a_code/pipelines/b3    a_backend/a_code/pipelines/pix
        |                                      |
        v                                      v
Bronze Parquet -> Silver Parquet -> Gold Parquet -> Reports
        |
        v
b_middleware/airflow e b_middleware/mcp como integracoes opcionais
```

## Estrutura

```text
a_backend/
├── a_code/
│   ├── common/
│   ├── interfaces/
│   ├── orchestration/
│   └── pipelines/
│       ├── b3/
│       └── pix/
├── b_data/
├── c_reports/
└── d_doc/
b_middleware/
├── airflow/
└── mcp/
d_test/
e_doc/
f_infra/
z_mis/
```

## Execucao

Instale as dependencias em ambiente virtual:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Execute um pipeline especifico:

```bash
python run_pipeline.py --pipeline b3
python run_pipeline.py --pipeline pix
```

Execute ambos:

```bash
python run_pipeline.py --pipeline all
```

Para execucao reduzida do Pix:

```bash
python run_pipeline.py --pipeline pix --pix-mode few --pix-rows 500
```

## Validacao

```bash
python -m compileall a_backend b_middleware run_pipeline.py
python -m a_backend.a_code.orchestration.validate_pipeline
```

## Decisoes Arquiteturais

- O repositorio foi classificado como `ms`, pois contem pipelines independentes e orquestraveis por dominio.
- B3 e Pix foram mantidos desacoplados para evitar mistura de regras de negocio.
- A camada `common/` concentra apenas componentes transversais.
- Airflow permanece como middleware opcional.
- MCP CSV permanece read-only e opcional.
- Notebooks Pix foram preservados; o core pode ser migrado gradualmente para Python puro nas proximas iteracoes.
- Dados processados e relatorios gerados devem ser reproduziveis e ignorados pelo Git.

## Fontes

- B3: Yahoo Finance e BRAPI, conforme configuracao do modulo B3.
- Pix: API OData de dados abertos do Banco Central do Brasil, com fallback para CSV publico manual.
