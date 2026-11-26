"""Configuración del proyecto.

Los valores por defecto sirven para desarrollo. Cualquiera se puede cambiar con una variable de
entorno con el prefijo ``CRS_`` (por ejemplo, ``CRS_RANDOM_SEED=7``).
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

ENV_PREFIX = "CRS_"
PROJECT_ROOT = Path(__file__).resolve().parents[2]


def _env(name: str, default: str) -> str:
    return os.environ.get(f"{ENV_PREFIX}{name}", default)


def _env_float(name: str, default: float) -> float:
    raw = _env(name, str(default))
    try:
        value = float(raw)
    except ValueError as exc:
        raise ValueError(f"{ENV_PREFIX}{name} debe ser un número, se recibió {raw!r}") from exc
    if value <= 0:
        raise ValueError(f"{ENV_PREFIX}{name} debe ser mayor que cero, se recibió {value}")
    return value


def _env_int(name: str, default: int) -> int:
    raw = _env(name, str(default))
    try:
        return int(raw)
    except ValueError as exc:
        raise ValueError(f"{ENV_PREFIX}{name} debe ser un entero, se recibió {raw!r}") from exc


@dataclass(frozen=True)
class Costs:
    """Costo relativo de cada tipo de error (ver ADR 0002)."""

    approve_defaulter: float
    """Aprobar a un cliente que no paga."""

    reject_good: float
    """Rechazar a un cliente que sí habría pagado."""


@dataclass(frozen=True)
class Settings:
    data_dir: Path
    models_dir: Path
    reports_dir: Path
    random_seed: int
    test_size: float
    log_level: str
    costs: Costs = field(repr=False)


def load_settings() -> Settings:
    """Lee la configuración desde variables de entorno, con valores por defecto."""
    test_size = _env_float("TEST_SIZE", 0.2)
    if not test_size < 1:
        raise ValueError(f"{ENV_PREFIX}TEST_SIZE debe estar entre 0 y 1, se recibió {test_size}")

    return Settings(
        data_dir=Path(_env("DATA_DIR", str(PROJECT_ROOT / "data"))),
        models_dir=Path(_env("MODELS_DIR", str(PROJECT_ROOT / "models"))),
        reports_dir=Path(_env("REPORTS_DIR", str(PROJECT_ROOT / "reports"))),
        random_seed=_env_int("RANDOM_SEED", 42),
        test_size=test_size,
        log_level=_env("LOG_LEVEL", "INFO").upper(),
        costs=Costs(
            approve_defaulter=_env_float("COST_APPROVE_DEFAULTER", 5.0),
            reject_good=_env_float("COST_REJECT_GOOD", 1.0),
        ),
    )
