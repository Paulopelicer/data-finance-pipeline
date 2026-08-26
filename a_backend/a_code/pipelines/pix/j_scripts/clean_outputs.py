"""Remove outputs e artefatos gerados pelo pipeline."""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

import shutil

from a_configs.config import (
    BASE_DIR,
    BRONZE_DIR,
    FIGURES_DIR,
    GOLD_DIR,
    PIPELINE_RUNS_DIR,
    SILVER_DIR,
    create_project_directories,
)

GENERATED_DIRS = [BRONZE_DIR, SILVER_DIR, GOLD_DIR, PIPELINE_RUNS_DIR]
GENERATED_PATTERNS = ["*.crc", "_SUCCESS", "*.pyc"]
CACHE_DIR_NAMES = ["__pycache__", ".ipynb_checkpoints", ".pytest_cache"]


def remove_path(path: Path) -> None:
    if path.is_dir():
        shutil.rmtree(path)
        print(f"Removido diretorio: {path.relative_to(BASE_DIR)}")
    elif path.exists():
        path.unlink()
        print(f"Removido arquivo: {path.relative_to(BASE_DIR)}")


def main() -> None:
    print("Limpando outputs gerados e artefatos temporarios.")

    for directory in GENERATED_DIRS:
        remove_path(directory)

    if FIGURES_DIR.exists():
        for figure in FIGURES_DIR.glob("*.png"):
            remove_path(figure)

    for pattern in GENERATED_PATTERNS:
        for path in BASE_DIR.rglob(pattern):
            if ".venv" not in path.parts and ".git" not in path.parts:
                remove_path(path)

    for cache_name in CACHE_DIR_NAMES:
        for path in BASE_DIR.rglob(cache_name):
            if ".venv" not in path.parts and ".git" not in path.parts:
                remove_path(path)

    create_project_directories(verbose=False)
    print("Limpeza concluida.")


if __name__ == "__main__":
    main()
