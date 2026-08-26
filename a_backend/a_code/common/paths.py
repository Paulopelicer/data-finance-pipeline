"""Caminhos centrais do projeto."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[3]
BACKEND_DIR = PROJECT_ROOT / "a_backend"
CODE_DIR = BACKEND_DIR / "a_code"
DATA_DIR = BACKEND_DIR / "b_data"
REPORTS_DIR = BACKEND_DIR / "c_reports"
DOC_DIR = BACKEND_DIR / "d_doc"
MIDDLEWARE_DIR = PROJECT_ROOT / "b_middleware"
TEST_DIR = PROJECT_ROOT / "d_test"
GENERAL_DOC_DIR = PROJECT_ROOT / "e_doc"
INFRA_DIR = PROJECT_ROOT / "f_infra"

B3_DOMAIN_DIR = CODE_DIR / "pipelines" / "b3"
PIX_DOMAIN_DIR = CODE_DIR / "pipelines" / "pix"

REQUIRED_DIRECTORIES = [
    DATA_DIR / "input" / "b3",
    DATA_DIR / "input" / "pix",
    DATA_DIR / "bronze" / "b3",
    DATA_DIR / "bronze" / "pix",
    DATA_DIR / "silver" / "b3",
    DATA_DIR / "silver" / "pix",
    DATA_DIR / "gold" / "b3",
    DATA_DIR / "gold" / "pix",
    REPORTS_DIR / "b3" / "pdf",
    REPORTS_DIR / "b3" / "figures",
    REPORTS_DIR / "pix" / "csv",
    REPORTS_DIR / "pix" / "figures",
]


def create_project_directories() -> None:
    """Cria diretorios operacionais esperados pela aplicacao consolidada."""
    for path in REQUIRED_DIRECTORIES:
        path.mkdir(parents=True, exist_ok=True)
