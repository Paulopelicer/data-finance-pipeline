"""Executa todos os notebooks do pipeline em ordem sequencial."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from src.config import BASE_DIR, FIGURES_DIR, NOTEBOOKS_DIR, PIPELINE_RUNS_DIR, create_project_directories
from src.spark_session import sanitize_spark_home
from scripts.clean_outputs import main as clean_outputs

NOTEBOOKS = [
    "01_bronze_ingestion_pix.ipynb",
    "02_silver_transform_pix.ipynb",
    "03_eda_pix.ipynb",
    "03_gold_indicators_pix.ipynb",
    "06_feature_engineering_pix.ipynb",
    "07_feature_selection_pix.ipynb",
    "08_prediction_regression_pix.ipynb",
    "09_prediction_classification_pix.ipynb",
    "04_fee_savings_estimation_pix.ipynb",
    "10_metrics_pix.ipynb",
    "05_data_viz_pix.ipynb",
]

REQUIRED_OUTPUTS = [
    BASE_DIR / "data" / "bronze" / "pix_raw" / "_SUCCESS",
    BASE_DIR / "data" / "silver" / "pix_clean" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_monthly_indicators" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_eda_summary" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_ml_features" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_selected_features" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_regression_predictions" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_classification_predictions" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_fee_savings_estimation" / "_SUCCESS",
    BASE_DIR / "data" / "gold" / "pix_transfer_savings_estimation" / "_SUCCESS",
    FIGURES_DIR / "01_pix_monthly_transactions.png",
    FIGURES_DIR / "02_pix_monthly_value.png",
    FIGURES_DIR / "03_pix_average_ticket.png",
    FIGURES_DIR / "04_pix_estimated_card_fee_savings.png",
    FIGURES_DIR / "05_pix_estimated_transfer_fee_savings.png",
    FIGURES_DIR / "06_pix_regression_real_vs_predicted.png",
    FIGURES_DIR / "07_pix_classification_confusion_matrix.png",
    FIGURES_DIR / "08_pix_eda_distribution_value.png",
    FIGURES_DIR / "09_pix_eda_distribution_transactions.png",
    FIGURES_DIR / "10_pix_feature_correlation_heatmap.png",
    BASE_DIR / "reports" / "regression_metrics.csv",
    BASE_DIR / "reports" / "classification_metrics.csv",
    BASE_DIR / "reports" / "model_metrics_summary.csv",
    BASE_DIR / "reports" / "business_metrics_summary.csv",
]


def build_env(rows: int | None = None) -> dict[str, str]:
    sanitize_spark_home()
    env = os.environ.copy()
    env.setdefault("MPLCONFIGDIR", "/tmp/matplotlib-pix")
    if rows:
        env["PIX_SAMPLE_ROWS"] = str(rows)
    spark_home = env.get("SPARK_HOME")
    if spark_home and not (Path(spark_home) / "bin" / "spark-submit").exists():
        env.pop("SPARK_HOME", None)
    return env


def execute_notebook(notebook_name: str, rows: int | None = None) -> None:
    print("=" * 78)
    print(f"Executando etapa: {notebook_name}")
    print("=" * 78)
    command = [
        sys.executable,
        "-m",
        "jupyter",
        "nbconvert",
        "--to",
        "notebook",
        "--execute",
        "--output-dir",
        str(PIPELINE_RUNS_DIR),
        "--ExecutePreprocessor.timeout=900",
        notebook_name,
    ]
    subprocess.run(command, cwd=NOTEBOOKS_DIR, env=build_env(rows), check=True)


def validate_required_outputs() -> None:
    missing = [path for path in REQUIRED_OUTPUTS if not path.exists()]
    if missing:
        print("Outputs obrigatorios ausentes:")
        for path in missing:
            print(f"- {path.relative_to(BASE_DIR)}")
        raise SystemExit(1)
    print("Todos os outputs obrigatorios foram gerados.")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Executa pipeline Pix completo.")
    parser.add_argument("--mode", choices=["all", "few"], default="all")
    parser.add_argument("--rows", type=int, default=None)
    args = parser.parse_args(argv)
    rows = args.rows if args.mode == "few" else None

    create_project_directories(verbose=False)
    clean_outputs()
    PIPELINE_RUNS_DIR.mkdir(parents=True, exist_ok=True)

    for notebook in NOTEBOOKS:
        execute_notebook(notebook, rows=rows)

    validate_required_outputs()
    print("Pipeline executado com sucesso.")


if __name__ == "__main__":
    main()
