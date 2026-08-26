"""Contrato comum para pipelines por dominio."""

from __future__ import annotations

from typing import Protocol


class PipelineRunner(Protocol):
    """Interface minima esperada de cada pipeline de dominio."""

    name: str

    def run(self) -> int:
        """Executa o pipeline completo e retorna codigo de saida."""
