import pytest
from services import plans

# Dummy plan data for testing purposes
dummy_plan_details = {
    "energyratestructure": [[{"rate": 0.1, "adj": 0.05}]],
    "fixedchargefirstmeter": 10,
    "fixedchargeunits": "$/month",
    "eiaid": 12345,
    "sector": "residential",
    "name": "Test Plan",
    "label": "test_label",
    "uri": "http://test.uri",
    "energyweekdayschedule": [[0] * 24],
    "energyweekendschedule": [[0] * 24]
}

dummy_hourly_rates = [0.1 for _ in range(24)]

# Verifies fixed plan JSON structure generation and correct fixedMonthlyCost calculation
def test_process_fixed_plan_to_json():
    result = plans.process_fixed_plan_to_json(
        rate=0.1,
        eia=12345,
        sector="residential",
        page_id="test_id",
        page_url="http://test.url",
        fixed_monthly_cost=10
    )

    assert result["ratePlanType"] == "fixed"
    assert result["fixedMonthlyCost"] == 120
    assert len(result["hourlyRates"]) == 24

# Verifies TOU plan JSON structure generation and correct fixedMonthlyCost calculation
def test_process_tou_plan_to_json():
    result = plans.process_tou_plan_to_json(
        hourly_rates=dummy_hourly_rates,
        eia=12345,
        sector="residential",
        page_id="test_id",
        page_url="http://test.url",
        fixed_monthly_cost=10
    )

    assert result["ratePlanType"] == "tou"
    assert result["fixedMonthlyCost"] == 120
    assert len(result["rates"]) == 3

# Verifies average rate calculation over specified hours with rounding applied
def test_calculate_average_rate():
    hours = [0, 1, 2]
    rates = [0.1 for _ in range(24)]
    avg = plans.calculate_average_rate(hours, rates)

    assert round(avg, 2) == 0.1

# Verifies conversion of time periods to the correct JSON hour range format
def test_convert_time_periods_to_json():
    result = plans.convert_time_periods_to_json([(0, 5), (6, 10)])
    assert result == [{"from": "00:00", "to": "05:00"}, {"from": "06:00", "to": "10:00"}]

# Verifies filtering plans by utility name returns only matching results
def test_filter_plans_by_utility():
    plans_list = [{"utility": "Utility A"}, {"utility": "Utility B"}]
    filtered = plans.filter_plans_by_utility(plans_list, "Utility A")

    assert len(filtered) == 1
    assert filtered[0]["utility"] == "Utility A"

# Verifies filtering plans by plan name returns only the matching result
def test_filter_plans_by_name():
    plans_list = [{"name": "Test Plan"}, {"name": "Other Plan"}]
    filtered = plans.filter_plans_by_name(plans_list, "Test Plan")

    assert len(filtered) == 1
    assert filtered[0]["name"] == "Test Plan"

# Verifies the generic fallback plan returns correct structure and hourly rates
def test_get_generic_plan():
    result = plans.get_generic_plan(sector="residential")

    assert result["ratePlanType"] == "tou"
    assert len(result["hourlyRates"]) == 24

# Verifies that a fixed-rate plan is processed correctly and includes hourly rates
def test_process_plans_fixed_rate():
    plans_list = [dummy_plan_details]
    result = plans.process_plans(plans_list, sector="residential")

    assert "Test Plan" in result
    assert "hourlyRates" in result["Test Plan"]

# Fixture that mocks the OpenEI API request for controlled test results
@pytest.fixture
def mock_make_openei_request(monkeypatch):
    def mock_request(*args, **kwargs):
        return {"items": [dummy_plan_details]}
    monkeypatch.setattr(plans, "make_openei_request", mock_request)

# Verifies that get_plan returns a valid plan dictionary with the correct sector and structure
def test_get_plan_returns_valid_result(mock_make_openei_request):
    result = plans.get_plan(latitude=0, longitude=0, name="Test Plan", sector="residential")

    assert isinstance(result, dict)
    assert result.get("sector") == "residential"
    assert "hourlyRates" in result
    assert result["ratePlanType"] in ["fixed", "tou"]  # Depends on dummy plan type

# ---------------- Value-Based Tests (Important Numerical Verifications) ----------------

# Ensures calculate_hourly_average_rate returns 24 averaged values across weekdays/weekends
def test_calculate_hourly_average_rate_output_length():
    result = plans.calculate_hourly_average_rate(dummy_plan_details)
    assert isinstance(result, list)
    assert len(result) == 24
    assert all(isinstance(r, float) for r in result)


# Ensures fallback plan is used when OpenEI returns no data
def test_get_plan_returns_fallback_if_no_data(monkeypatch):
    monkeypatch.setattr(plans, "make_openei_request", lambda *args, **kwargs: {"items": []})
    result = plans.get_plan(latitude=0, longitude=0, name="Missing Plan", sector="residential")
    assert result["ratePlanType"] == "tou"
    assert "hourlyRates" in result


# Validates filtering by utility returns empty if none match
def test_filter_plans_by_utility_no_match():
    plans_list = [{"utility": "Other"}]
    filtered = plans.filter_plans_by_utility(plans_list, "Missing Utility")
    assert filtered == []
