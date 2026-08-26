"""Validacoes compartilhadas de estrutura e outputs."""

from __future__ import annotations

from pathlib import Path


def ensure_path_exists(path: Path, label: str) -> None:
    if not path.exists():
        raise FileNotFoundError(f"{label} nao encontrado: {path}")


def ensure_non_empty_directory(path: Path, label: str) -> None:
    ensure_path_exists(path, label)
    if not any(path.iterdir()):
        raise ValueError(f"{label} esta vazio: {path}")


def ensure_columns(columns: list[str], required_columns: list[str], label: str) -> None:
    missing = [column for column in required_columns if column not in columns]
    if missing:
        raise ValueError(f"{label} sem colunas obrigatorias: {missing}")
