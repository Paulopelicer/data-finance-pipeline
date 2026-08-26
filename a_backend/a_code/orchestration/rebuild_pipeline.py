"""Rebuild local da aplicacao consolidada."""

from __future__ import annotations

from a_backend.a_code.orchestration.clean_outputs import main as clean_outputs
from a_backend.a_code.orchestration.run_pipeline import main as run_pipeline


def main() -> int:
    clean_outputs()
    return run_pipeline(["--pipeline", "all"])


if __name__ == "__main__":
    raise SystemExit(main())
