# B3 Data Platform

> Financial data lakehouse for B3 (Brazilian Stock Exchange) using the **Medallion Architecture** (Bronze → Silver → Gold).

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://www.python.org/)
[![Polars](https://img.shields.io/badge/Polars-Latest-orange.svg)](https://pola.rs/)
[![PySpark](https://img.shields.io/badge/PySpark-3.5-red.svg)](https://spark.apache.org/)

---

## Architecture Overview

This platform implements a **Medallion Architecture** (Bronze-Silver-Gold) for processing Brazilian stock market data:

```mermaid
flowchart LR
    %% Data Sources
    YF[Yahoo Finance API]
    BRAPI[BRAPI]

    %% Ingestion
    YF --> ING[Ingestion Layer]
    BRAPI --> ING

    %% Bronze Layer
    ING --> BRONZE[(Bronze Layer<br/>Raw Data<br/>Parquet)]

    %% Silver Layer
    BRONZE --> ETL[ETL Processing<br/>- Deduplication<br/>- Validation<br/>- Enrichment]
    ETL --> SILVER[(Silver Layer<br/>Clean Data<br/>Parquet)]

    %% Gold Layer
    SILVER --> AGG[Aggregation<br/>Polars · PySpark<br/>- Daily Metrics<br/>- Portfolio Summary<br/>- Monthly Returns]
    AGG --> GOLD[(Gold Layer<br/>Analytics<br/>Parquet)]

    %% Consumption
    GOLD --> NB[Jupyter Notebooks<br/>Interactive Analysis]
    GOLD --> RPT[PDF Reports<br/>Automated Insights]
    GOLD --> VIZ[Visualizations<br/>Charts & Dashboards]

    %% Orchestration
    AIRFLOW[Apache Airflow<br/>Orchestration] -.-> ING
    AIRFLOW -.-> ETL
    AIRFLOW -.-> AGG

    %% Storage
    MINIO[MinIO<br/>S3-Compatible Storage] -.-> BRONZE
    MINIO -.-> SILVER
    MINIO -.-> GOLD

    style BRONZE fill:#cd7f32,stroke:#333,stroke-width:2px,color:#fff
    style SILVER fill:#c0c0c0,stroke:#333,stroke-width:2px,color:#000
    style GOLD fill:#ffd700,stroke:#333,stroke-width:2px,color:#000
    style AIRFLOW fill:#017cee,stroke:#333,stroke-width:2px,color:#fff
    style MINIO fill:#c72e49,stroke:#333,stroke-width:2px,color:#fff
```

### Medallion Layers Explained

| Layer      | Description                        | Data Quality                    | Use Case                       |
| ---------- | ---------------------------------- | ------------------------------- | ------------------------------ |
| **Bronze** | Raw data as-is from sources        | Low - No transformations        | Audit trail, reprocessing      |
| **Silver** | Cleaned, deduplicated, validated   | Medium - Business rules applied | Analytics queries, ML features |
| **Gold**   | Aggregated, business-ready metrics | High - Production-ready         | Reports, dashboards, KPIs      |

---

## Stack

| Component        | Tool                      | Purpose                              |
| ---------------- | ------------------------- | ------------------------------------ |
| Processing       | **Polars** + **PySpark**  | Transformations (medium & large vol) |
| Orchestration    | **Apache Airflow**        | DAG per layer, retry & sensors       |
| Storage          | **MinIO** (local S3)      | Object storage for Parquet files     |
| Notebooks        | **JupyterLab**            | Interactive exploration              |
| Visualisation    | **Plotly** + **Seaborn**  | Charts inside notebooks              |
| Data source      | **Yahoo Finance** / BRAPI | B3 daily OHLCV prices                |
| Containerisation | **Docker Compose**        | Full local environment               |

OHLCV = Open, High, Low, Close, Volume (Abertura, Máxima, Mínima, Fechamento, Volume)

---

## Project Structure

Top-level folders follow a `<letter>_<name>` ordering pattern so they
appear in the logical data-flow order in the file tree.

```
b3-data-plataform/
├── a_configs/          # Settings, Spark factory, MinIO client, JSON logger
├── b_models/           # Pydantic models + Spark schemas
├── c_ingestion/        # Yahoo Finance + BRAPI adapters
├── d_processing/
│   ├── a_bronze/       # Raw writer / reader
│   ├── b_silver/       # ETL transformations
│   ├── c_gold/         # Aggregations (daily metrics, portfolio, monthly)
│   └── d_report/       # PDF report generation with charts
├── e_validation/       # Quality checks (fail-fast assertions)
├── f_pipelines/        # Bronze / Silver / Gold pipeline classes
├── g_storage/          # Storage adapters (Parquet / Delta / DB)
├── h_dags/             # Airflow DAGs (Bronze → Silver → Gold chain)
├── i_notebooks/        # 01 Bronze · 02 Silver · 03 Gold · 04 Exploration
├── j_data/             # Local Parquet store (Medallion layers)
│   ├── a_bronze/       # Raw ingested data (partitioned by trade_date)
│   ├── b_silver/       # Cleaned & validated data
│   └── c_gold/         # Aggregated analytics-ready tables
├── k_logs/             # Application logs (JSON structured)
├── l_tests/            # pytest unit tests + conftest fixtures
├── m_docs/             # Project documentation (PRDs, architecture)
├── n_reports/          # Generated PDF reports
├── z_infra/            # Docker infrastructure
│   ├── docker-compose.yml    # MinIO + PostgreSQL + Airflow + JupyterLab
│   ├── Dockerfile.airflow    # Custom Airflow image
│   └── .dockerignore         # Docker build exclusions
├── z_scripts/          # Utility/debug scripts
├── run_pipeline.py     # One-command full pipeline execution
├── setup.sh            # Setup & management script (Linux/macOS/WSL)
├── setup.bat           # Windows launcher
└── requirements.txt    # Python dependencies
```

---

## Quick Start

### 1 — Local (no Docker)

```bash
# Create virtual environment
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Copy env file
cp .env.example .env

# Option 1: Run complete pipeline with one command (recommended)
python run_pipeline.py

# Option 2: Run each layer manually
python -c "
from f_pipelines.a_bronze_pipeline import BronzePipeline
from f_pipelines.b_silver_pipeline import SilverPipeline
from f_pipelines.c_gold_pipeline import GoldPipeline
from f_pipelines.d_report_pipeline import ReportPipeline

BronzePipeline().run()   # Ingest raw data
SilverPipeline().run()   # Clean & transform
GoldPipeline().run()     # Aggregate metrics
ReportPipeline().run()   # Generate PDF report
"

# Start JupyterLab for interactive exploration
jupyter lab i_notebooks/
```

**Pipeline Execution Output:**

```
================================================================================
B3 DATA PLATFORM - FULL PIPELINE EXECUTION
================================================================================

[1/4] Running Bronze Pipeline (Data Ingestion)...
Bronze complete: 2988 rows ingested

[2/4] Running Silver Pipeline (Data Transformation)...
Silver complete

[3/4] Running Gold Pipeline (Analytics & Aggregation)...
Gold complete

[4/4] Running Report Pipeline (PDF Generation)...
Report complete: /path/to/report_260720_1509.pdf

================================================================================
PIPELINE EXECUTION COMPLETE!
================================================================================
```

### 2 — Docker Compose (full stack)

```bash
# Using the automated setup script (recommended)
./setup.sh setup     # Full setup
./setup.sh up        # Start containers only
./setup.sh down      # Stop containers
./setup.sh status    # Check status
./setup.sh logs      # View logs

# Or manually
cd z_infra
docker compose up -d

# Services:
#   JupyterLab  →  http://localhost:8888  (token: b3data)
#   Airflow UI  →  http://localhost:8080  (user/pass: admin/admin)
#   MinIO UI    →  http://localhost:9001  (user/pass: minioadmin/minioadmin)
```

### 3 — Run tests

```bash
pytest -v
```

---

## Notebooks

| #   | Notebook                    | Description                             |
| --- | --------------------------- | --------------------------------------- |
| 01  | `01_bronze_ingestion.ipynb` | Ingest raw prices, inspect Bronze layer |
| 02  | `02_silver_etl.ipynb`       | Step-by-step ETL, quality checks        |
| 03  | `03_gold_analytics.ipynb`   | Cumulative return, volatility, heatmaps |
| 04  | `04_exploration.ipynb`      | Correlation, Bollinger Bands, Spark SQL |

---

## Airflow DAGs

| DAG                     | Schedule          | Description           |
| ----------------------- | ----------------- | --------------------- |
| `a_b3_bronze_ingestion` | Mon–Fri 22:00 UTC | Fetch prices → Bronze |
| `b_b3_silver_etl`       | Mon–Fri 22:30 UTC | Bronze → Silver ETL   |
| `c_b3_gold_aggregation` | Mon–Fri 23:00 UTC | Silver → Gold tables  |

DAGs use `ExternalTaskSensor` so Silver waits for Bronze and Gold waits for Silver.

---

## Tracked Tickers (default)

`PETR4` · `VALE3` · `ITUB4` · `BBDC4` · `ABEV3` · `WEGE3` · `RENT3` · `MGLU3` · `BPAC11` · `LREN3` · `BBAS3` · `RADL3`

Override via `DEFAULT_TICKERS` in `a_configs/settings.py` or pass a custom list to whichever pipeline you run.

---

## AI Agents & Automation

This project uses **VS Code Copilot agents, skills, and prompts** (defined in `.github/`) to accelerate development with AI-assisted workflows.

### Available Agents

| Agent                 | Purpose                                           |
| --------------------- | ------------------------------------------------- |
| Pipeline Generator    | Generate complete end-to-end pipelines            |
| Data Quality Reviewer | Validate data, audit schemas, quality checks      |
| Maintenance Debugger  | Diagnose failures, fix bugs, optimize performance |
| Airflow Orchestrator  | Create DAGs, configure scheduling & dependencies  |
| Test Engineer         | Create pytest tests, fixtures, ensure coverage    |

Invoke in Copilot Chat: `@Pipeline Generator crie uma pipeline para dados da CVM`

### Skills (Domain Knowledge)

Skills provide specialized context that agents reference automatically:

| Skill                      | Domain                               |
| -------------------------- | ------------------------------------ |
| Polars Data Processing     | Polars transformations & idioms      |
| Medallion Architecture     | Bronze→Silver→Gold contracts         |
| Pydantic & Spark Schemas   | Explicit models and schemas          |
| Financial Data Engineering | B3 financial calculations            |
| Data Quality & Validation  | Fail-fast quality checks             |
| Airflow DAG Patterns       | Orchestration patterns               |
| Python Project Conventions | Code style & project conventions     |
| Report Generation          | PDF generation with FPDF2/Matplotlib |
| Storage & Infrastructure   | MinIO, Parquet, Docker               |

### Prompts (Quick Actions)

| Prompt         | Action                                      |
| -------------- | ------------------------------------------- |
| New Pipeline   | Create a complete pipeline for a new source |
| Debug Pipeline | Diagnose and fix pipeline failures          |
| Add Ticker     | Add a new ticker to the portfolio           |
| Create Tests   | Generate tests for an existing module       |
| Review Project | Full compliance review                      |
| New Gold Table | Add an analytical Gold table                |

Use via Command Palette: **Copilot: Use Prompt** → select the prompt.

### Lifecycle Commands

| Command     | When to Use                             | Primary Agent/Skill          |
| ----------- | --------------------------------------- | ---------------------------- |
| `/spec`     | Define a new data source or table       | Pipeline Generator           |
| `/plan`     | List tasks and files to create          | Pipeline Generator           |
| `/build`    | Implement code                          | Pipeline Generator + Skills  |
| `/validate` | Run quality checks and tests            | Data Quality + Test Engineer |
| `/review`   | Compliance audit                        | Data Quality Reviewer        |
| `/debug`    | Diagnose a failure                      | Maintenance Debugger         |
| `/ship`     | Prepare for deploy (lint + tests + DAG) | All                          |

### Recommended Workflow

```
1. /spec     → Define what will be built
2. /plan     → List files and tasks
3. /build    → Implement with @Pipeline Generator
4. /validate → Test with @Test Engineer + @Data Quality Reviewer
5. /review   → Audit with review-project prompt
6. /ship     → Lint + Tests + Deploy
```

### Design Principles

1. **Spec before code** — Define before implementing
2. **Contract-first** — Schemas and quality checks before logic
3. **Idempotent** — Every execution is re-runnable without side effects
4. **Fail-fast** — Error detected = pipeline stops immediately
5. **Observable** — Structured logs at every step
6. **Testable** — Every module has a corresponding test

---

## Configuration

All configuration is centralized in `.env` file:

```env
# Data Paths
DATA_PATH_BRONZE=j_data/a_bronze
DATA_PATH_SILVER=j_data/b_silver
DATA_PATH_GOLD=j_data/c_gold

# MinIO / S3
MINIO_ENDPOINT=http://localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Airflow
AIRFLOW_ADMIN_USER=admin
AIRFLOW_ADMIN_PASSWORD=admin
```

---
