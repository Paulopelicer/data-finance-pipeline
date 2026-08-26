"""Ferramentas read-only para consulta segura de CSVs analiticos do projeto."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_DIR = Path(__file__).resolve().parents[2]
REPORTS_DIR = PROJECT_DIR / "reports"
METRICS_FILES = [
    "business_metrics_summary.csv",
    "classification_metrics.csv",
    "feature_correlation_matrix.csv",
    "feature_selection_summary.csv",
    "model_metrics_summary.csv",
    "regression_metrics.csv",
]


def _safe_csv_path(file_name: str | Path) -> Path:
    raw = Path(str(file_name))
    if raw.is_absolute():
        raise ValueError("Caminhos absolutos nao sao permitidos.")
    if ".." in raw.parts:
        raise ValueError("Path traversal com '..' nao e permitido.")
    if raw.suffix.lower() != ".csv":
        raise ValueError("Somente arquivos .csv sao permitidos.")

    candidate = (PROJECT_DIR / raw).resolve() if raw.parts and raw.parts[0] == "reports" else (REPORTS_DIR / raw).resolve()
    reports_root = REPORTS_DIR.resolve()
    if not candidate.is_relative_to(reports_root):
        raise ValueError("Leitura fora da pasta reports nao e permitida.")
    if not candidate.exists():
        raise FileNotFoundError(f"Arquivo CSV nao encontrado: {candidate.relative_to(PROJECT_DIR)}")
    return candidate


def _relative(path: Path) -> str:
    return str(path.relative_to(PROJECT_DIR))


def _approx_line_count(path: Path, limit: int = 100_000) -> int:
    count = 0
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        for count, _line in enumerate(handle, start=1):
            if count >= limit:
                break
    return count


def csv_list_reports() -> dict[str, Any]:
    """Lista arquivos CSV disponiveis em reports."""
    files = []
    if REPORTS_DIR.exists():
        for path in sorted(REPORTS_DIR.glob("*.csv")):
            files.append(
                {
                    "name": path.name,
                    "path": _relative(path),
                    "size_bytes": path.stat().st_size,
                    "approx_lines": _approx_line_count(path),
                }
            )
    return {"reports_dir": "reports", "csv_files": files, "count": len(files)}


def csv_preview_file(file_name: str, rows: int = 5) -> dict[str, Any]:
    """Retorna as primeiras linhas de um CSV seguro."""
    path = _safe_csv_path(file_name)
    max_rows = max(1, min(int(rows), 20))
    frame = pd.read_csv(path, nrows=max_rows)
    return {
        "file": _relative(path),
        "rows_returned": len(frame),
        "columns": list(frame.columns),
        "data": frame.fillna("").to_dict(orient="records"),
    }


def csv_describe_file(file_name: str) -> dict[str, Any]:
    """Descreve colunas, tipos e estatisticas basicas de um CSV."""
    path = _safe_csv_path(file_name)
    frame = pd.read_csv(path)
    numeric = frame.select_dtypes(include="number")
    return {
        "file": _relative(path),
        "row_count": int(len(frame)),
        "column_count": int(len(frame.columns)),
        "columns": list(frame.columns),
        "dtypes": {column: str(dtype) for column, dtype in frame.dtypes.items()},
        "numeric_summary": numeric.describe().fillna("").to_dict() if not numeric.empty else {},
    }


def csv_validate_columns(file_name: str, columns: list[str] | str) -> dict[str, Any]:
    """Valida se um CSV contem as colunas esperadas."""
    path = _safe_csv_path(file_name)
    expected = [item.strip() for item in columns.split(",")] if isinstance(columns, str) else list(columns)
    expected_set = set(expected)
    found = list(pd.read_csv(path, nrows=0).columns)
    found_set = set(found)
    missing = sorted(expected_set - found_set)
    extra = sorted(found_set - expected_set)
    return {
        "file": _relative(path),
        "expected_columns": expected,
        "found_columns": found,
        "missing_columns": missing,
        "extra_columns": extra,
        "valid": not missing,
    }


def csv_get_metrics_summary() -> dict[str, Any]:
    """Resume os principais CSVs de metricas gerados pelo pipeline."""
    found: dict[str, Any] = {}
    missing = []
    for file_name in METRICS_FILES:
        path = REPORTS_DIR / file_name
        if not path.exists():
            missing.append(file_name)
            continue
        frame = pd.read_csv(path)
        found[file_name] = {
            "rows": int(len(frame)),
            "columns": list(frame.columns),
            "preview": frame.head(5).fillna("").to_dict(orient="records"),
        }
    return {
        "metrics_found": sorted(found.keys()),
        "metrics_missing": missing,
        "business_metrics": found.get("business_metrics_summary.csv", {}),
        "regression_metrics": found.get("regression_metrics.csv", {}),
        "classification_metrics": found.get("classification_metrics.csv", {}),
        "feature_selection": found.get("feature_selection_summary.csv", {}),
        "files": found,
    }


def csv_search_value(query: str, max_results: int = 20) -> dict[str, Any]:
    """Busca termo textual simples nos CSVs de reports."""
    if not query or not query.strip():
        raise ValueError("A consulta nao pode ser vazia.")
    term = query.strip().lower()
    limit = max(1, min(int(max_results), 50))
    results = []
    for path in sorted(REPORTS_DIR.glob("*.csv")):
        with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
            reader = csv.reader(handle)
            for line_number, row in enumerate(reader, start=1):
                text = " | ".join(row)
                if term in text.lower():
                    results.append({"file": _relative(path), "line": line_number, "text": text[:500]})
                    if len(results) >= limit:
                        return {"query": query, "results": results, "truncated": True}
    return {"query": query, "results": results, "truncated": False}


def csv_compare_metrics_files() -> dict[str, Any]:
    """Compara arquivos de metricas e consolida dimensoes basicas."""
    comparison = []
    for file_name in ["regression_metrics.csv", "classification_metrics.csv", "model_metrics_summary.csv"]:
        path = REPORTS_DIR / file_name
        if not path.exists():
            comparison.append({"file": file_name, "exists": False})
            continue
        frame = pd.read_csv(path)
        comparison.append(
            {
                "file": file_name,
                "exists": True,
                "rows": int(len(frame)),
                "columns": list(frame.columns),
                "numeric_columns": list(frame.select_dtypes(include="number").columns),
            }
        )
    return {"comparison": comparison}


TOOLS = {
    "csv_list_reports": csv_list_reports,
    "csv_preview_file": csv_preview_file,
    "csv_describe_file": csv_describe_file,
    "csv_validate_columns": csv_validate_columns,
    "csv_get_metrics_summary": csv_get_metrics_summary,
    "csv_search_value": csv_search_value,
    "csv_compare_metrics_files": csv_compare_metrics_files,
}

