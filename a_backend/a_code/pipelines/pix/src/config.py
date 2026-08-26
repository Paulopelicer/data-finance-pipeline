"""Configuracao centralizada de caminhos do projeto Pix Data Pipeline."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
BRONZE_DIR = DATA_DIR / "bronze"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"

REPORTS_DIR = BASE_DIR / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
DOCS_DIR = BASE_DIR / "docs"
NOTEBOOKS_DIR = BASE_DIR / "notebooks"
SCRIPTS_DIR = BASE_DIR / "scripts"
TESTS_DIR = BASE_DIR / "tests"
PIPELINE_RUNS_DIR = BASE_DIR / ".pipeline_runs"
AGENTS_SKILLS_DIR = BASE_DIR / "agents_skills"

PIX_RAW_DIR = BRONZE_DIR / "pix_raw"
PIX_RAW_SAMPLE_CSV = BRONZE_DIR / "pix_raw_sample.csv"
PIX_CLEAN_DIR = SILVER_DIR / "pix_clean"
PIX_MONTHLY_INDICATORS_DIR = GOLD_DIR / "pix_monthly_indicators"
PIX_MONTHLY_INDICATORS_CSV_DIR = GOLD_DIR / "pix_monthly_indicators_csv"
PIX_FEE_SAVINGS_DIR = GOLD_DIR / "pix_fee_savings_estimation"
PIX_TRANSFER_SAVINGS_DIR = GOLD_DIR / "pix_transfer_savings_estimation"
PIX_EDA_SUMMARY_DIR = GOLD_DIR / "pix_eda_summary"
PIX_ML_FEATURES_DIR = GOLD_DIR / "pix_ml_features"
PIX_ML_FEATURES_CSV_DIR = GOLD_DIR / "pix_ml_features_csv"
PIX_SELECTED_FEATURES_DIR = GOLD_DIR / "pix_selected_features"
PIX_REGRESSION_PREDICTIONS_DIR = GOLD_DIR / "pix_regression_predictions"
PIX_CLASSIFICATION_PREDICTIONS_DIR = GOLD_DIR / "pix_classification_predictions"

REQUIRED_DIRECTORIES = [
    DATA_DIR,
    INPUT_DIR,
    BRONZE_DIR,
    PIX_RAW_DIR,
    SILVER_DIR,
    PIX_CLEAN_DIR,
    GOLD_DIR,
    PIX_MONTHLY_INDICATORS_DIR,
    PIX_MONTHLY_INDICATORS_CSV_DIR,
    PIX_FEE_SAVINGS_DIR,
    PIX_TRANSFER_SAVINGS_DIR,
    PIX_EDA_SUMMARY_DIR,
    PIX_ML_FEATURES_DIR,
    PIX_ML_FEATURES_CSV_DIR,
    PIX_SELECTED_FEATURES_DIR,
    PIX_REGRESSION_PREDICTIONS_DIR,
    PIX_CLASSIFICATION_PREDICTIONS_DIR,
    REPORTS_DIR,
    FIGURES_DIR,
    DOCS_DIR,
    NOTEBOOKS_DIR,
    SCRIPTS_DIR,
    TESTS_DIR,
]


def create_project_directories(verbose: bool = False) -> None:
    """Cria as pastas operacionais necessarias para o pipeline."""
    for directory in REQUIRED_DIRECTORIES:
        directory.mkdir(parents=True, exist_ok=True)
        if verbose:
            print(f"Diretorio pronto: {directory.relative_to(BASE_DIR)}")


if __name__ == "__main__":
    create_project_directories(verbose=True)
