"""Valida outputs do pipeline para apresentacao local no VSCode."""

from pathlib import Path
import sys

PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR))

from src.config import (  # noqa: E402
    FIGURES_DIR,
    PIX_CLEAN_DIR,
    PIX_FEE_SAVINGS_DIR,
    PIX_MONTHLY_INDICATORS_DIR,
    PIX_RAW_DIR,
    PIX_TRANSFER_SAVINGS_DIR,
)
from src.spark_session import get_spark_session  # noqa: E402


def print_section(title: str) -> None:
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def validate_layer(spark, name: str, path: Path) -> None:
    df = spark.read.parquet(str(path))
    print(f"{name:<35} {df.count():>8} registros  {path}")


def main() -> None:
    spark = get_spark_session("pix-presentation-demo")
    try:
        print_section("Validacao local do pipeline Pix")
        validate_layer(spark, "Bronze / pix_raw", PIX_RAW_DIR)
        validate_layer(spark, "Silver / pix_clean", PIX_CLEAN_DIR)
        validate_layer(spark, "Gold / monthly_indicators", PIX_MONTHLY_INDICATORS_DIR)
        validate_layer(spark, "Gold / fee_savings", PIX_FEE_SAVINGS_DIR)
        validate_layer(spark, "Gold / transfer_savings", PIX_TRANSFER_SAVINGS_DIR)

        print_section("Amostra da camada Gold")
        monthly = spark.read.parquet(str(PIX_MONTHLY_INDICATORS_DIR))
        monthly.orderBy("ano_mes").show(10, truncate=False)

        print_section("Graficos disponiveis")
        for figure in sorted(FIGURES_DIR.glob("*.png")):
            size_kb = figure.stat().st_size / 1024
            print(f"{figure.name:<45} {size_kb:>8.1f} KB")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()
