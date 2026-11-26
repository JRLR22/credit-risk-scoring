from pathlib import Path

import pytest

from credit_risk.config import PROJECT_ROOT, load_settings


def test_defaults(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("DATA_DIR", "RANDOM_SEED", "TEST_SIZE", "LOG_LEVEL"):
        monkeypatch.delenv(f"CRS_{name}", raising=False)

    settings = load_settings()

    assert settings.data_dir == PROJECT_ROOT / "data"
    assert settings.random_seed == 42
    assert settings.test_size == 0.2
    assert settings.log_level == "INFO"
    assert settings.costs.approve_defaulter == 5.0
    assert settings.costs.reject_good == 1.0


def test_environment_overrides_defaults(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("CRS_DATA_DIR", str(tmp_path))
    monkeypatch.setenv("CRS_RANDOM_SEED", "7")
    monkeypatch.setenv("CRS_LOG_LEVEL", "debug")
    monkeypatch.setenv("CRS_COST_APPROVE_DEFAULTER", "3")

    settings = load_settings()

    assert settings.data_dir == tmp_path
    assert settings.random_seed == 7
    assert settings.log_level == "DEBUG"
    assert settings.costs.approve_defaulter == 3.0


@pytest.mark.parametrize(
    ("name", "value"),
    [
        ("RANDOM_SEED", "abc"),
        ("TEST_SIZE", "1.5"),
        ("TEST_SIZE", "0"),
        ("COST_REJECT_GOOD", "-1"),
        ("COST_APPROVE_DEFAULTER", "mucho"),
    ],
)
def test_invalid_values_are_rejected(
    monkeypatch: pytest.MonkeyPatch, name: str, value: str
) -> None:
    monkeypatch.setenv(f"CRS_{name}", value)

    with pytest.raises(ValueError, match=f"CRS_{name}"):
        load_settings()
