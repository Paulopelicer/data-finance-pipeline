"""Validacoes simples de qualidade de dados para o pipeline Pix."""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F


def ensure_not_empty(df: DataFrame, name: str) -> None:
    """Falha se o DataFrame estiver vazio."""
    if df.rdd.isEmpty():
        raise ValueError(f"DataFrame vazio: {name}")


def ensure_columns(df: DataFrame, required_columns: list[str], name: str) -> None:
    """Falha se colunas obrigatorias estiverem ausentes."""
    missing = [column for column in required_columns if column not in df.columns]
    if missing:
        raise ValueError(f"Colunas ausentes em {name}: {missing}")


def filter_non_negative(df: DataFrame, columns: list[str]) -> DataFrame:
    """Remove registros com valores negativos nas colunas indicadas."""
    condition = None
    for column in columns:
        current = F.col(column).isNull() | (F.col(column) >= 0)
        condition = current if condition is None else condition & current
    return df.filter(condition) if condition is not None else df
