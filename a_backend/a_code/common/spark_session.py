"""Criacao compartilhada de SparkSession."""

from __future__ import annotations

import os
from pathlib import Path


def sanitize_spark_home() -> None:
    """Remove SPARK_HOME invalido para permitir uso do PySpark do ambiente."""
    spark_home = os.environ.get("SPARK_HOME")
    if spark_home and not (Path(spark_home) / "bin" / "spark-submit").exists():
        os.environ.pop("SPARK_HOME", None)


def get_spark_session(app_name: str):
    """Cria uma SparkSession local com configuracao conservadora."""
    sanitize_spark_home()
    from pyspark.sql import SparkSession

    return (
        SparkSession.builder.appName(app_name)
        .master(os.environ.get("SPARK_MASTER", "local[*]"))
        .config("spark.sql.execution.arrow.pyspark.enabled", "true")
        .config("spark.sql.parquet.datetimeRebaseModeInRead", "CORRECTED")
        .config("spark.sql.parquet.datetimeRebaseModeInWrite", "CORRECTED")
        .getOrCreate()
    )
