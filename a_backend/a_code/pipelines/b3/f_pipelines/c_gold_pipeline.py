"""
Gold pipeline — builds analytical tables from Silver data.

Supports two processing engines via ``GoldPipelineConfig.engine``:
- ``"polars"`` (default): fast, single-node, zero-dependency aggregation.
- ``"spark"``: distributed aggregation via PySpark + Spark SQL,
  suited for large-volume workloads.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import polars as pl

from a_configs.logger import get_logger
from d_processing.b_silver.transform import read_silver
from d_processing.c_gold.aggregate import (
    build_daily_metrics,
    build_monthly_returns,
    build_portfolio_summary,
    write_gold,
)

logger = get_logger(__name__)


@dataclass
class GoldPipelineConfig:
    trade_date: str | None = None  # None → all available Silver data
    engine: Literal["polars", "spark"] = field(default="polars")


class GoldPipeline:
    """
    Read Silver → build analytical Gold tables → persist.

    Tables produced:
    - ``daily_metrics``:     per (ticker, trade_date) with rolling features
    - ``portfolio_summary``: one row per ticker, period aggregates
    - ``monthly_returns``:   monthly OHLC + returns per ticker

    Set ``engine="spark"`` to use PySpark for aggregation (requires Spark).
    """

    def __init__(self, config: GoldPipelineConfig | None = None):
        self.config = config or GoldPipelineConfig()

    def extract(self) -> pl.DataFrame:
        logger.info("Reading Silver data for Gold pipeline")
        return read_silver(trade_date=self.config.trade_date)

    def _transform_polars(self, df: pl.DataFrame) -> dict[str, pl.DataFrame]:
        daily = build_daily_metrics(df)
        summary = build_portfolio_summary(daily)
        monthly = build_monthly_returns(df)
        return {
            "daily_metrics": daily,
            "portfolio_summary": summary,
            "monthly_returns": monthly,
        }

    def _transform_spark(self, df: pl.DataFrame) -> dict[str, pl.DataFrame]:
        from d_processing.c_gold.aggregate_spark import (
            build_daily_metrics_spark,
            build_monthly_returns_spark,
            build_portfolio_summary_spark,
            polars_to_spark,
            spark_to_polars,
        )

        spark_df = polars_to_spark(df)
        daily_spark = build_daily_metrics_spark(spark_df)
        summary_spark = build_portfolio_summary_spark(daily_spark)
        monthly_spark = build_monthly_returns_spark(spark_df)

        return {
            "daily_metrics": spark_to_polars(daily_spark),
            "portfolio_summary": spark_to_polars(summary_spark),
            "monthly_returns": spark_to_polars(monthly_spark),
        }

    def transform(self, df: pl.DataFrame) -> dict[str, pl.DataFrame]:
        logger.info(
            "Building Gold tables",
            extra={"input_rows": len(df), "engine": self.config.engine},
        )
        if self.config.engine == "spark":
            return self._transform_spark(df)
        return self._transform_polars(df)

    def load(self, tables: dict[str, pl.DataFrame]) -> None:
        for name, df in tables.items():
            write_gold(df, table=name)

    def run(self) -> dict[str, pl.DataFrame]:
        logger.info("GoldPipeline started", extra={"engine": self.config.engine})
        silver_df = self.extract()
        if silver_df.is_empty():
            logger.warning("Silver layer is empty — nothing to aggregate")
            return {}
        tables = self.transform(silver_df)
        self.load(tables)
        for name, df in tables.items():
            logger.info("Gold table ready", extra={"table": name, "rows": len(df)})
        logger.info("GoldPipeline finished")
        return tables
