"""Configuracao central da aplicacao consolidada."""

from __future__ import annotations

from dataclasses import dataclass

from a_backend.a_code.common.paths import PROJECT_ROOT


@dataclass(frozen=True)
class ProjectConfig:
    name: str = "stf_pss_ms_data_finance_pipeline"
    root: object = PROJECT_ROOT
    default_pipeline: str = "all"


CONFIG = ProjectConfig()
