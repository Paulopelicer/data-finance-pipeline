"""Funcoes reutilizaveis para features e metricas do pipeline Pix."""

from __future__ import annotations

from math import sqrt


def calculate_ticket_medio(valor_total: float, quantidade_transacoes: float) -> float | None:
    """Calcula ticket medio com protecao para divisor nulo ou zero."""
    if quantidade_transacoes in (None, 0):
        return None
    return valor_total / quantidade_transacoes


def calculate_growth_percent(current_value: float, previous_value: float) -> float | None:
    """Calcula crescimento percentual com protecao para base nula ou zero."""
    if previous_value in (None, 0) or current_value is None:
        return None
    return ((current_value - previous_value) / previous_value) * 100


def calculate_card_savings(valor_total_pix: float, percentual_substituicao: float, taxa_mdr: float) -> float:
    """Calcula economia potencial estimada com taxa de cartao."""
    return valor_total_pix * percentual_substituicao * taxa_mdr


def calculate_transfer_savings(quantidade_transacoes_pix: float, percentual_substituicao: float, tarifa_referencia: float) -> float:
    """Calcula economia potencial estimada com transferencia tradicional."""
    return quantidade_transacoes_pix * percentual_substituicao * tarifa_referencia


def calculate_rmse(mse: float) -> float:
    """Calcula RMSE a partir do MSE."""
    return sqrt(mse)
