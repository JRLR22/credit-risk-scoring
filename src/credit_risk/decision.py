"""Reglas para convertir una probabilidad de impago en una decisión."""

from credit_risk.config import Costs


def decision_threshold(costs: Costs) -> float:
    """Probabilidad de impago a partir de la cual conviene rechazar (ver ADR 0002)."""
    return costs.reject_good / (costs.approve_defaulter + costs.reject_good)
