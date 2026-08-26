"""Logging comum para a aplicacao consolidada."""

from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    """Retorna logger com formato simples e consistente."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s - %(message)s",
    )
    return logging.getLogger(name)
