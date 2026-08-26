"""Validador estrutural da aplicacao consolidada."""

from __future__ import annotations

from pathlib import Path

from a_backend.a_code.common.config import CONFIG
from a_backend.a_code.common.paths import PROJECT_ROOT


REQUIRED_PATHS = [
    "a_backend/a_code/common",
    "a_backend/a_code/pipelines/b3/run_pipeline.py",
    "a_backend/a_code/pipelines/b3/f_pipelines",
    "a_backend/a_code/pipelines/b3/d_processing",
    "a_backend/a_code/pipelines/pix/run_pipeline.py",
    "a_backend/a_code/pipelines/pix/src",
    "a_backend/a_code/pipelines/pix/notebooks",
    "b_middleware/airflow/dags",
    "b_middleware/mcp",
    "d_test/b_test_unit",
    "e_doc/1_SPC",
    "f_infra/a_docker",
    "README.md",
    "pyproject.toml",
    "requirements.txt",
]


def validate_required_paths(errors: list[str]) -> None:
    for relative_path in REQUIRED_PATHS:
        path = PROJECT_ROOT / relative_path
        if not path.exists():
            errors.append(f"Caminho obrigatorio ausente: {relative_path}")


def validate_no_frontend(errors: list[str]) -> None:
    frontend = PROJECT_ROOT / "c_frontend"
    if frontend.exists():
        errors.append("Pasta c_frontend nao deve existir neste projeto.")


def validate_project_name(errors: list[str]) -> None:
    pyproject = PROJECT_ROOT / "pyproject.toml"
    readme = PROJECT_ROOT / "README.md"
    for path in [pyproject, readme]:
        if path.exists() and CONFIG.name not in path.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"Nome do projeto ausente em {path.relative_to(PROJECT_ROOT)}")


def validate_no_windows_absolute_paths(errors: list[str]) -> None:
    for path in [PROJECT_ROOT / "README.md", PROJECT_ROOT / "pyproject.toml"]:
        if path.exists() and "C:\\" in path.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"Caminho absoluto Windows encontrado em {path.relative_to(PROJECT_ROOT)}")


def main() -> int:
    errors: list[str] = []
    validate_required_paths(errors)
    validate_no_frontend(errors)
    validate_project_name(errors)
    validate_no_windows_absolute_paths(errors)

    if errors:
        print("Validacao estrutural falhou:")
        for error in errors:
            print(f"- {error}")
        return 1

    print("Validacao estrutural concluida com sucesso.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
