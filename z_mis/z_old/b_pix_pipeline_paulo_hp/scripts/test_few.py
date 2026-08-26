"""Executa teste de sistema com amostra pequena da fonte publica."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from scripts.rebuild_pipeline import main as rebuild_main


def main() -> None:
    parser = argparse.ArgumentParser(description="Executa pipeline Pix com amostra reduzida.")
    parser.add_argument("--rows", type=int, default=500)
    args = parser.parse_args()
    rebuild_main(["--mode", "few", "--rows", str(args.rows)])


if __name__ == "__main__":
    main()
