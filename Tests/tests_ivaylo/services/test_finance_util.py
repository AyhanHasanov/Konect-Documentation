import pytest
import pandas as pd
from services.finance_util import get_hourly_proportions, predict_visits_by_hour


# Tests if the returned proportions are a pandas Series of length 24 and sum to ~1.
def test_get_hourly_proportions():
    proportions = get_hourly_proportions()

    assert isinstance(proportions, pd.Series), "Expected a pandas Series"
    assert len(proportions) == 24, "Expected 24 hourly entries"

    total = proportions.sum()
    assert abs(total - 1.0) < 1e-6, f"Proportions should sum to 1 got {total}"

# Tests that the predicted visits list has 24 items and the sum equals the weekly_visits input.
@pytest.mark.parametrize("weekly_visits", [100, 500, 1234])
def test_predict_visits_by_hour(weekly_visits):
    hourly_visits = predict_visits_by_hour(weekly_visits)

    assert isinstance(hourly_visits, list), "Expected output to be a list"
    assert len(hourly_visits) == 24, "Expected 24 predicted values"

    total_predicted = sum(hourly_visits)
    assert abs(total_predicted - weekly_visits) < 1e-4, (
        f"Sum of predicted visits should equal input ({weekly_visits}), got {total_predicted}"
    )

# ---------------- Value-Based Tests (Important Numerical Verifications) ----------------

# Tests get_hourly_proportions returns non-negative values and values are between 0 and 1.
def test_hourly_proportions_are_valid():
    proportions = get_hourly_proportions()
    assert all(0 <= p <= 1 for p in proportions), "Proportions should be between 0 and 1"


# Tests predict_visits_by_hour correctly handles zero weekly visits.
def test_predict_visits_by_hour_zero_case():
    hourly_visits = predict_visits_by_hour(0)
    assert sum(hourly_visits) == 0, "Expected all hourly visits to be zero when weekly visits are zero"
    assert all(v == 0 for v in hourly_visits), "All hourly values should be zero"


# Tests predict_visits_by_hour with fractional weekly visits to ensure proper handling.
def test_predict_visits_by_hour_fractional_input():
    weekly_visits = 123.45
    hourly_visits = predict_visits_by_hour(weekly_visits)
    total_predicted = sum(hourly_visits)
    assert abs(total_predicted - weekly_visits) < 1e-4, (
        f"Sum of predicted visits should equal input ({weekly_visits}), got {total_predicted}"
    )


# Tests that predicted visits are proportionally distributed based on known proportions.
def test_predict_visits_by_hour_proportionality():
    weekly_visits = 2400
    hourly_visits = predict_visits_by_hour(weekly_visits)
    max_hour_value = max(hourly_visits)
    min_hour_value = min(hourly_visits)

    assert max_hour_value > min_hour_value, "There should be variance in hourly predictions reflecting proportions"
