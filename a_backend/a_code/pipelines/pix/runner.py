"""Runner do pipeline Pix migrado."""

from __future__ import annotations

import subprocess
import sys

from a_backend.a_code.common.paths import PIX_DOMAIN_DIR


def run(mode: str = "all", rows: int | None = None) -> int:
    """Executa o pipeline Pix preservando seu contexto de modulo original."""
    command = [sys.executable, "run_pipeline.py", "--mode", mode]
    if rows is not None:
        command.extend(["--rows", str(rows)])
    return subprocess.run(command, cwd=PIX_DOMAIN_DIR, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(run())
