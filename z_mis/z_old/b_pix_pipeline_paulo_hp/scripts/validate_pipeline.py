"""Valida estrutura, codigo e outputs do pipeline Pix."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from src.config import (
    BASE_DIR,
    FIGURES_DIR,
    NOTEBOOKS_DIR,
    PIX_CLASSIFICATION_PREDICTIONS_DIR,
    PIX_CLEAN_DIR,
    PIX_EDA_SUMMARY_DIR,
    PIX_FEE_SAVINGS_DIR,
    PIX_ML_FEATURES_DIR,
    PIX_MONTHLY_INDICATORS_DIR,
    PIX_RAW_DIR,
    PIX_REGRESSION_PREDICTIONS_DIR,
    PIX_SELECTED_FEATURES_DIR,
    PIX_TRANSFER_SAVINGS_DIR,
    create_project_directories,
)
from src.spark_session import get_spark_session

REQUIRED_FILES = [
    "README.md", "requirements.txt", ".gitignore", "run_pipeline.py",
    "src/config.py", "src/spark_session.py", "src/data_source.py", "src/data_quality.py", "src/utils.py", "src/feature_engineering.py",
    "scripts/clean_outputs.py", "scripts/rebuild_pipeline.py", "scripts/validate_pipeline.py", "scripts/test_few.py", "scripts/validate_agents_skills.py",
    "scripts/validate_mcp_csv.py", "scripts/sync_agents_skills_to_codex.py",
    "data/input/README_input.md", "docs/PRD_Functional.md", "docs/PRD_Technical.md", "docs/guardrails.md", "docs/code_guardrails.md",
    "docs/requirements_traceability_matrix.md", "docs/agent_skills_research.md", "docs/agents_inventory.md", "docs/agent_interaction_examples.md",
    "mcp/README.md", "mcp/csv_mcp_server.py", "mcp/tools/csv_tools.py", "mcp/mcp_config.example.json",
    "reports/regression_metrics.csv", "reports/classification_metrics.csv", "reports/model_metrics_summary.csv", "reports/business_metrics_summary.csv",
]

REQUIRED_NOTEBOOKS = [
    "00_run_all.ipynb", "01_bronze_ingestion_pix.ipynb", "02_silver_transform_pix.ipynb", "03_eda_pix.ipynb",
    "03_gold_indicators_pix.ipynb", "04_fee_savings_estimation_pix.ipynb", "05_data_viz_pix.ipynb",
    "06_feature_engineering_pix.ipynb", "07_feature_selection_pix.ipynb", "08_prediction_regression_pix.ipynb",
    "09_prediction_classification_pix.ipynb", "10_metrics_pix.ipynb",
]

REQUIRED_DIRS = [
    "data/input", "data/bronze", "data/silver", "data/gold", "notebooks", "reports/figures", "src", "scripts", "docs", "tests", "docs/knowledge_base", "agents_skills", "mcp", "mcp/tools",
]

REQUIRED_OUTPUTS = [
    PIX_RAW_DIR / "_SUCCESS", PIX_CLEAN_DIR / "_SUCCESS", PIX_MONTHLY_INDICATORS_DIR / "_SUCCESS",
    PIX_EDA_SUMMARY_DIR / "_SUCCESS", PIX_ML_FEATURES_DIR / "_SUCCESS", PIX_SELECTED_FEATURES_DIR / "_SUCCESS",
    PIX_REGRESSION_PREDICTIONS_DIR / "_SUCCESS", PIX_CLASSIFICATION_PREDICTIONS_DIR / "_SUCCESS",
    PIX_FEE_SAVINGS_DIR / "_SUCCESS", PIX_TRANSFER_SAVINGS_DIR / "_SUCCESS",
    FIGURES_DIR / "01_pix_monthly_transactions.png", FIGURES_DIR / "02_pix_monthly_value.png", FIGURES_DIR / "03_pix_average_ticket.png",
    FIGURES_DIR / "04_pix_estimated_card_fee_savings.png", FIGURES_DIR / "05_pix_estimated_transfer_fee_savings.png",
    FIGURES_DIR / "06_pix_regression_real_vs_predicted.png", FIGURES_DIR / "07_pix_classification_confusion_matrix.png",
    FIGURES_DIR / "08_pix_eda_distribution_value.png", FIGURES_DIR / "09_pix_eda_distribution_transactions.png",
    FIGURES_DIR / "10_pix_feature_correlation_heatmap.png",
]

REQUIRED_GITIGNORE_PATTERNS = ["__pycache__/", "*.pyc", ".ipynb_checkpoints/", ".venv/", ".metastore_db/", "derby.log", "spark-warehouse/", "*.crc", "_SUCCESS", ".pipeline_runs/", ".pytest_cache/", "reports/figures/*.png", "data/bronze/", "data/silver/", "data/gold/"]
TEXT_PATTERNS_TO_SCAN = ["*.py", "*.md", "*.ipynb", "*.json", "*.yaml"]
EXCLUDED_PARTS = {".venv", ".git", ".pipeline_runs", "__pycache__", "data"}
EMOJI_RE = re.compile("[" "\U0001F300-\U0001FAFF" "\U00002700-\U000027BF" "\U00002600-\U000026FF" "]")
WINDOWS_PATH_RE = re.compile(
    r"(?:[A-Za-z]:\\(?:Users|Windows|Program Files|ProgramData|Temp|tmp)|/mnt/" + "c/Users/)",
    re.IGNORECASE,
)
DISALLOWED_SIMULATION_RE = re.compile(r"dados\s+" + r"simulad[oa]s" + "|" + r"fonte\s+" + r"simulad[oa]", re.IGNORECASE)


def rel(path: Path) -> str:
    return str(path.relative_to(BASE_DIR))


def fail(message: str, errors: list[str]) -> None:
    errors.append(message)
    print(f"FALHA: {message}")


def pass_msg(message: str) -> None:
    print(f"OK: {message}")


def iter_text_files():
    for pattern in TEXT_PATTERNS_TO_SCAN:
        for path in BASE_DIR.rglob(pattern):
            if any(part in EXCLUDED_PARTS for part in path.parts):
                continue
            yield path


def validate_files(errors: list[str]) -> None:
    for item in REQUIRED_FILES:
        path = BASE_DIR / item
        pass_msg(f"arquivo encontrado: {item}") if path.exists() else fail(f"arquivo ausente: {item}", errors)
    for item in REQUIRED_NOTEBOOKS:
        path = NOTEBOOKS_DIR / item
        pass_msg(f"notebook encontrado: {item}") if path.exists() else fail(f"notebook ausente: {item}", errors)
    for item in REQUIRED_DIRS:
        path = BASE_DIR / item
        pass_msg(f"diretorio encontrado: {item}") if path.exists() and path.is_dir() else fail(f"diretorio ausente: {item}", errors)


def validate_notebooks_json(errors: list[str]) -> None:
    for name in REQUIRED_NOTEBOOKS:
        path = NOTEBOOKS_DIR / name
        if not path.exists():
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
            pass_msg(f"JSON valido: notebooks/{name}")
        except Exception as exc:
            fail(f"JSON invalido em notebooks/{name}: {exc}", errors)


def validate_text_quality(errors: list[str]) -> None:
    for path in iter_text_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        relative = rel(path)
        if EMOJI_RE.search(text):
            fail(f"emoji encontrado em {relative}", errors)
        if WINDOWS_PATH_RE.search(text):
            fail(f"caminho absoluto local proibido encontrado em {relative}", errors)
        if path.suffix in {".py", ".ipynb"} and DISALLOWED_SIMULATION_RE.search(text):
            fail(f"referencia a fonte ficticia na execucao em {relative}", errors)
    pass_msg("arquivos principais verificados quanto a emojis e caminhos absolutos")


def validate_gitignore(errors: list[str]) -> None:
    gitignore_path = BASE_DIR / ".gitignore"
    if not gitignore_path.exists():
        fail(".gitignore ausente", errors)
        return
    patterns = {line.strip() for line in gitignore_path.read_text(encoding="utf-8").splitlines() if line.strip() and not line.strip().startswith("#")}
    missing = [pattern for pattern in REQUIRED_GITIGNORE_PATTERNS if pattern not in patterns]
    fail(f".gitignore sem padroes obrigatorios: {missing}", errors) if missing else pass_msg(".gitignore contem caches, outputs e artefatos Spark")


def validate_outputs(errors: list[str]) -> None:
    for path in REQUIRED_OUTPUTS:
        pass_msg(f"output encontrado: {rel(path)}") if path.exists() else fail(f"output ausente: {rel(path)}", errors)
    if errors:
        return
    spark = get_spark_session("pix-pipeline-validation")
    checks = [("Bronze", PIX_RAW_DIR), ("Silver", PIX_CLEAN_DIR), ("Gold indicadores", PIX_MONTHLY_INDICATORS_DIR), ("Gold EDA", PIX_EDA_SUMMARY_DIR), ("Gold features", PIX_ML_FEATURES_DIR), ("Gold selected features", PIX_SELECTED_FEATURES_DIR), ("Gold regressao", PIX_REGRESSION_PREDICTIONS_DIR), ("Gold classificacao", PIX_CLASSIFICATION_PREDICTIONS_DIR), ("Gold economia cartao", PIX_FEE_SAVINGS_DIR), ("Gold economia transferencia", PIX_TRANSFER_SAVINGS_DIR)]
    try:
        for label, path in checks:
            count = spark.read.parquet(str(path)).count()
            pass_msg(f"{label} possui {count} registros") if count > 0 else fail(f"{label} esta vazio", errors)
    finally:
        spark.stop()


def main() -> int:
    create_project_directories(verbose=False)
    errors: list[str] = []
    validate_files(errors)
    validate_notebooks_json(errors)
    validate_text_quality(errors)
    validate_gitignore(errors)
    validate_outputs(errors)
    if errors:
        print("Validacao concluida com falhas.")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Validacao concluida com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
