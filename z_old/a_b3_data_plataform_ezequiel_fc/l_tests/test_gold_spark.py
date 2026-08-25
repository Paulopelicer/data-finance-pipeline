"""
Unit tests for Gold layer — PySpark-based aggregations.
"""
from __future__ import annotations

import pytest
import polars as pl

from d_processing.c_gold.aggregate_spark import (
    build_daily_metrics_spark,
    build_monthly_returns_spark,
    build_portfolio_summary_spark,
    polars_to_spark,
    spark_to_polars,
)


@pytest.fixture(scope="module")
def spark():
    """Shared SparkSession for the test module (reused across tests)."""
    from a_configs.spark_config import create_spark_session

    session = create_spark_session(app_name="test-gold-spark")
    yield session
    session.stop()


@pytest.fixture
def spark_silver_df(silver_df, spark):
    """Silver data as a Spark DataFrame."""
    return polars_to_spark(silver_df)


# ---------------------------------------------------------------------------
# Conversion round-trip
# ---------------------------------------------------------------------------


def test_polars_to_spark_preserves_rows(silver_df, spark_silver_df):
    assert spark_silver_df.count() == len(silver_df)


def test_spark_to_polars_preserves_rows(silver_df, spark_silver_df):
    result = spark_to_polars(spark_silver_df)
    assert len(result) == len(silver_df)


# ---------------------------------------------------------------------------
# build_daily_metrics_spark
# ---------------------------------------------------------------------------


def test_daily_metrics_spark_adds_cum_return(spark_silver_df):
    result = build_daily_metrics_spark(spark_silver_df)
    assert "cum_return" in result.columns


def test_daily_metrics_spark_adds_year_month(spark_silver_df):
    result = build_daily_metrics_spark(spark_silver_df)
    assert "year" in result.columns
    assert "month" in result.columns


def test_daily_metrics_spark_avg_volume_present(spark_silver_df):
    result = build_daily_metrics_spark(spark_silver_df)
    assert "avg_volume_20d" in result.columns


def test_daily_metrics_spark_volatility_present(spark_silver_df):
    result = build_daily_metrics_spark(spark_silver_df)
    assert "volatility_20d" in result.columns


def test_daily_metrics_spark_row_count_preserved(silver_df, spark_silver_df):
    result = build_daily_metrics_spark(spark_silver_df)
    assert result.count() == len(silver_df)


# ---------------------------------------------------------------------------
# build_portfolio_summary_spark
# ---------------------------------------------------------------------------


def test_portfolio_summary_spark_one_row_per_ticker(silver_df, spark_silver_df):
    metrics = build_daily_metrics_spark(spark_silver_df)
    summary = build_portfolio_summary_spark(metrics)
    assert summary.count() == silver_df["ticker"].n_unique()


def test_portfolio_summary_spark_has_required_columns(spark_silver_df):
    metrics = build_daily_metrics_spark(spark_silver_df)
    summary = build_portfolio_summary_spark(metrics)
    required = {"ticker", "first_date", "last_date", "total_return", "avg_daily_volume"}
    assert required.issubset(set(summary.columns))


# ---------------------------------------------------------------------------
# build_monthly_returns_spark
# ---------------------------------------------------------------------------


def test_monthly_returns_spark_has_month_return(spark_silver_df):
    result = build_monthly_returns_spark(spark_silver_df)
    assert "month_return" in result.columns


def test_monthly_returns_spark_grouped_correctly(silver_df, spark_silver_df):
    result = build_monthly_returns_spark(spark_silver_df)
    expected_groups = silver_df.with_columns(
        pl.col("trade_date").dt.year().alias("year"),
        pl.col("trade_date").dt.month().alias("month"),
    ).select(["ticker", "year", "month"]).n_unique()
    assert result.count() == expected_groups


# ---------------------------------------------------------------------------
# GoldPipeline with engine="spark"
# ---------------------------------------------------------------------------


def test_gold_pipeline_spark_engine_config():
    from f_pipelines.c_gold_pipeline import GoldPipelineConfig

    config = GoldPipelineConfig(engine="spark")
    assert config.engine == "spark"


def test_gold_pipeline_default_engine_is_polars():
    from f_pipelines.c_gold_pipeline import GoldPipelineConfig

    config = GoldPipelineConfig()
    assert config.engine == "polars"
