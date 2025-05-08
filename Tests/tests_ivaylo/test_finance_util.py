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