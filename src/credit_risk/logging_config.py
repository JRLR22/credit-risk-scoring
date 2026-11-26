"""Configuración de logging compartida por los scripts, la API y el tablero."""

from __future__ import annotations

import logging

LOG_FORMAT = "%(asctime)s %(levelname)s %(name)s: %(message)s"


def setup_logging(level: str = "INFO") -> None:
    """Configura el logger raíz. Se puede llamar varias veces sin duplicar mensajes."""
    numeric_level = logging.getLevelName(level.upper())
    if not isinstance(numeric_level, int):
        raise ValueError(f"Nivel de log desconocido: {level!r}")
    logging.basicConfig(level=numeric_level, format=LOG_FORMAT, force=True)
