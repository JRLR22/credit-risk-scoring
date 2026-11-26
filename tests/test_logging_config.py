import logging

import pytest

from credit_risk.logging_config import setup_logging


def test_sets_root_level() -> None:
    setup_logging("debug")
    assert logging.getLogger().level == logging.DEBUG

    setup_logging("WARNING")
    assert logging.getLogger().level == logging.WARNING


def test_does_not_duplicate_handlers() -> None:
    setup_logging()
    setup_logging()
    assert len(logging.getLogger().handlers) == 1


def test_unknown_level_is_rejected() -> None:
    with pytest.raises(ValueError, match="Nivel de log"):
        setup_logging("ruidoso")
