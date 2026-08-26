"""Helpers minimos para I/O Parquet."""

from __future__ import annotations

from pathlib import Path


def parquet_success_marker(path: Path) -> Path:
    """Retorna o marcador padrao de sucesso de escrita Spark."""
    return path / "_SUCCESS"
