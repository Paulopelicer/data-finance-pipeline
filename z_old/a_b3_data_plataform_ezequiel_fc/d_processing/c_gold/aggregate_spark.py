"""
Gold layer — analytical aggregations using PySpark.
Spark-based alternative to the Polars Gold aggregations, designed for
large-volume analytical workloads.

Produces the same three tables as the Polars version:
  - daily_metrics
  - portfolio_summary
  - monthly_returns
"""
from __future__ import annotations

from pathlib import Path

from pyspark.sql import DataFrame as SparkDataFrame
from pyspark.sql import Window
from pyspark.sql import functions as F

from a_configs.logger import get_logger
from a_configs.settings import DATA_PATH_GOLD
from a_configs.spark_config import create_spark_session

logger = get_logger(__name__)


# ---------------------------------------------------------------------------
# Aggregation functions
# ---------------------------------------------------------------------------


def build_daily_metrics_spark(df: SparkDataFrame) -> SparkDataFrame:
    """
    Enrich each (ticker, trade_date) row with rolling analytical features:
    - avg_volume_20d: 20-trading-day rolling average volume
    - volatility_20d: 20-day rolling stddev of daily_return (annualised × √252)
    - cum_return: cumulative return from the first trade date
    - year, month: calendar partitioning helpers
    """
    ticker_window = Window.partitionBy("ticker").orderBy("trade_date")
    rolling_20 = (
        Window.partitionBy("ticker")
        .orderBy("trade_date")
        .rowsBetween(-19, Window.currentRow)
    )

    df = df.withColumn(
        "avg_volume_20d", F.avg("volume").over(rolling_20)
    ).withColumn(
        "volatility_20d",
        F.stddev("daily_return").over(rolling_20) * F.lit(252 ** 0.5),
    ).withColumn(
        "year", F.year("trade_date"),
    ).withColumn(
        "month", F.month("trade_date"),
    )

    # Cumulative return per ticker (compound): product of (1 + r) - 1
    # Spark has no cum_prod, so we use log/exp trick:
    # cum_prod(1+r) = exp(sum(ln(1+r)))
    df = df.withColumn(
        "_log_factor",
        F.log(F.lit(1.0) + F.coalesce(F.col("daily_return"), F.lit(0.0))),
    ).withColumn(
        "cum_return",
        F.exp(F.sum("_log_factor").over(ticker_window)) - F.lit(1.0),
    ).drop("_log_factor")

    return df


def build_portfolio_summary_spark(df: SparkDataFrame) -> SparkDataFrame:
    """
    Aggregate to one row per ticker with:
    - first/last trade date
    - total cumulative return
    - average daily volume
    - average annualised volatility
    - period high/low
    """
    return (
        df.groupBy("ticker")
        .agg(
            F.min("trade_date").alias("first_date"),
            F.max("trade_date").alias("last_date"),
            F.last("cum_return").alias("total_return"),
            F.avg("volume").alias("avg_daily_volume"),
            F.avg("volatility_20d").alias("avg_volatility"),
            F.max("close_price").alias("period_high"),
            F.min("close_price").alias("period_low"),
        )
        .orderBy(F.col("total_return").desc())
    )


def build_monthly_returns_spark(df: SparkDataFrame) -> SparkDataFrame:
    """
    Monthly OHLC-style aggregation per ticker:
    uses first open and last close of each month.
    """
    df = df.withColumn("year", F.year("trade_date")).withColumn(
        "month", F.month("trade_date")
    )

    return (
        df.groupBy("ticker", "year", "month")
        .agg(
            F.first("open_price").alias("month_open"),
            F.last("close_price").alias("month_close"),
            F.max("high_price").alias("month_high"),
            F.min("low_price").alias("month_low"),
            F.sum("volume").alias("month_volume"),
            F.avg("daily_return").alias("avg_daily_return"),
        )
        .withColumn(
            "month_return",
            (F.col("month_close") / F.col("month_open")) - F.lit(1.0),
        )
        .orderBy("ticker", "year", "month")
    )


# ---------------------------------------------------------------------------
# I/O helpers
# ---------------------------------------------------------------------------


def write_gold_spark(df: SparkDataFrame, table: str) -> Path:
    """Write a Gold table as Parquet using Spark."""
    output_path = DATA_PATH_GOLD / table
    output_path.mkdir(parents=True, exist_ok=True)

    if "year" in df.columns and "month" in df.columns:
        (
            df.write.mode("overwrite")
            .partitionBy("year", "month")
            .parquet(str(output_path))
        )
    else:
        df.write.mode("overwrite").parquet(str(output_path))

    row_count = df.count()
    logger.info(
        "Gold Spark write complete",
        extra={"table": table, "rows": row_count, "output": str(output_path)},
    )
    return output_path


def polars_to_spark(df: "pl.DataFrame") -> SparkDataFrame:
    """Convert a Polars DataFrame to a Spark DataFrame via Arrow."""
    import polars as pl

    spark = create_spark_session()
    arrow_table = df.to_arrow()
    return spark.createDataFrame(arrow_table.to_pandas(), schema=None)


def spark_to_polars(df: SparkDataFrame) -> "pl.DataFrame":
    """Convert a Spark DataFrame to a Polars DataFrame via Pandas."""
    import polars as pl

    return pl.from_pandas(df.toPandas())
