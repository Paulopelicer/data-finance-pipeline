"""Runner do pipeline B3 migrado."""

from __future__ import annotations

import subprocess
import sys

from a_backend.a_code.common.paths import B3_DOMAIN_DIR


def run() -> int:
    """Executa o pipeline B3 preservando seu contexto de modulo original."""
    command = [sys.executable, "run_pipeline.py"]
    return subprocess.run(command, cwd=B3_DOMAIN_DIR, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(run())
