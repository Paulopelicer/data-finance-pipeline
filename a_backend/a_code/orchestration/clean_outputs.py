"""Limpeza idempotente de outputs gerados."""

from __future__ import annotations

import shutil

from a_backend.a_code.common.paths import DATA_DIR, REPORTS_DIR


def main() -> int:
    for path in [DATA_DIR / "bronze", DATA_DIR / "silver", DATA_DIR / "gold", REPORTS_DIR]:
        if path.exists():
            shutil.rmtree(path)
    print("Outputs consolidados removidos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
