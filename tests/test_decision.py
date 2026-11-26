import pytest

from credit_risk.config import Costs
from credit_risk.decision import decision_threshold


def test_threshold_with_project_costs() -> None:
    costs = Costs(approve_defaulter=5, reject_good=1)
    assert decision_threshold(costs) == pytest.approx(1 / 6)


def test_threshold_with_equal_costs() -> None:
    costs = Costs(approve_defaulter=1, reject_good=1)
    assert decision_threshold(costs) == pytest.approx(0.5)


def test_threshold_with_higher_cost_of_default() -> None:
    costs = Costs(approve_defaulter=3, reject_good=1)
    assert decision_threshold(costs) == pytest.approx(0.25)
