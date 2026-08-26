"""Factory para criacao de SparkSession local."""

import os
from pathlib import Path

from pyspark.sql import SparkSession


def sanitize_spark_home() -> None:
    """Remove SPARK_HOME do ambiente quando aponta para instalacao inexistente."""
    spark_home = os.environ.get("SPARK_HOME")
    if "SPARK_HOME" in os.environ and (
        not spark_home or not (Path(spark_home) / "bin" / "spark-submit").exists()
    ):
        os.environ.pop("SPARK_HOME", None)


def get_spark_session(app_name: str = "pix-data-pipeline-spark") -> SparkSession:
    """Cria ou retorna uma SparkSession local para execucao em WSL."""
    sanitize_spark_home()

    spark = (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .config("spark.sql.session.timeZone", "America/Sao_Paulo")
        .config("spark.sql.adaptive.enabled", "true")
        .config("spark.sql.adaptive.coalescePartitions.enabled", "true")
        .getOrCreate()
    )
    spark.sparkContext.setLogLevel("WARN")
    return spark


if __name__ == "__main__":
    session = get_spark_session("pix-data-pipeline-spark-test")
    print(f"SparkSession criada. Versao Spark: {session.version}")
    session.stop()
