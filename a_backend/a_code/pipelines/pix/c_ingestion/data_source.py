"""Funcoes para ingestao de dados publicos reais do Pix."""

from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import time
from typing import Iterable

import pandas as pd
import requests

from a_configs.config import INPUT_DIR

BCB_PIX_TRANSACTIONS_URL = (
    "https://olinda.bcb.gov.br/olinda/servico/Pix_DadosAbertos/versao/v1/odata/"
    "EstatisticasTransacoesPix(Database=@Database)?@Database='202401'&$top=50000&$format=json"
)

REQUIRED_PIX_COLUMNS = {"AnoMes", "VALOR", "QUANTIDADE"}


@dataclass(frozen=True)
class SourceResult:
    """Resultado de uma ingestao de fonte publica."""

    data: pd.DataFrame
    source_type: str
    source_reference: str


def _validate_pix_dataframe(df: pd.DataFrame, source_reference: str) -> None:
    if df.empty:
        raise ValueError(f"Fonte sem registros: {source_reference}")

    missing = REQUIRED_PIX_COLUMNS.difference(df.columns)
    if missing:
        raise ValueError(
            "Fonte publica sem colunas obrigatorias "
            f"{sorted(missing)}. Fonte: {source_reference}"
        )


def _apply_sample_limit(df: pd.DataFrame) -> pd.DataFrame:
    rows = os.environ.get("PIX_SAMPLE_ROWS")
    if not rows:
        return df
    try:
        limit = int(rows)
    except ValueError:
        return df
    if limit > 0:
        print(f"Aplicando amostra de teste com {limit} registros.")
        return df.head(limit)
    return df


def fetch_bcb_pix_transactions(timeout: int = 120, attempts: int = 3) -> SourceResult:
    """Baixa dados reais publicos de transacoes Pix pelo OData do Banco Central."""
    last_error: Exception | None = None
    for attempt in range(1, attempts + 1):
        try:
            print(
                f"Tentativa {attempt}/{attempts} de leitura da fonte publica do Banco Central."
            )
            response = requests.get(BCB_PIX_TRANSACTIONS_URL, timeout=timeout)
            response.raise_for_status()
            break
        except requests.RequestException as exc:
            last_error = exc
            if attempt < attempts:
                time.sleep(5)
            else:
                raise RuntimeError(
                    "Falha apos retentativas na fonte publica do Banco Central."
                ) from last_error
    payload = response.json()
    records = payload.get("value", [])
    df = pd.DataFrame(records)
    df = _apply_sample_limit(df)
    _validate_pix_dataframe(df, BCB_PIX_TRANSACTIONS_URL)
    return SourceResult(df, "url_publica_banco_central", BCB_PIX_TRANSACTIONS_URL)


def _manual_csv_files(input_dir: Path = INPUT_DIR) -> Iterable[Path]:
    return sorted(input_dir.glob("*.csv"))


def load_manual_public_csv(input_dir: Path = INPUT_DIR) -> SourceResult:
    """Carrega arquivo CSV publico colocado manualmente em data/input."""
    for csv_path in _manual_csv_files(input_dir):
        df = pd.read_csv(csv_path, sep=None, engine="python")
        df = _apply_sample_limit(df)
        _validate_pix_dataframe(df, str(csv_path))
        return SourceResult(df, "csv_publico_manual", str(csv_path))

    raise FileNotFoundError(
        "Nenhum CSV publico foi encontrado em data/input. "
        "Baixe um CSV publico do Banco Central com colunas AnoMes, VALOR e QUANTIDADE."
    )


def load_public_pix_data() -> SourceResult:
    """Tenta fonte publica automatica e usa CSV publico manual como fallback."""
    try:
        return fetch_bcb_pix_transactions()
    except Exception as exc:
        print(f"Falha na ingestao automatica do Banco Central: {exc}")
        print("Tentando fallback por CSV publico manual em data/input.")
        return load_manual_public_csv()
