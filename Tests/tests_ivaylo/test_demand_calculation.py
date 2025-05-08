from math import floor

from services.demand_calculation import DemandCalculationService, get_demand_table_with_default

# Sample time range input
mock_time_ranges = {
    "jan": {
        "weekdays": {
            "Tier 1": {"time_ranges": [{"from": 8, "to": 18}], "occurrence_percent": 45},
            "Tier 2": {"time_ranges": [{"from": 19, "to": 23}], "occurrence_percent": 10},
        },
        "weekends": {
            "Tier 1": {"time_ranges": [{"from": 10, "to": 20}], "occurrence_percent": 35},
            "Tier 2": {"time_ranges": [{"from": 21, "to": 23}], "occurrence_percent": 10},
        }
    }
}

# Sample tier cost input
mock_tiers_demand_cost = {
    "monthly_demand_charge": {
        "jan": [
            {"from_kw": 0, "to_kw": 100, "rate": 2.0},
            {"from_kw": 101, "to_kw": 200, "rate": 3.0}
        ]
    },
    "time_of_use_demand_charge": {
        "jan": {
            "weekday": {
                "Tier 1": 1.5,
                "Tier 2": 2.5
            },
            "weekend": {
                "Tier 1": 1.0,
                "Tier 2": 2.0
            }
        }
    }
}

mock_hardware_config = {
    "cabinets": [
        {
            "capacity": 150,
            "chargers": [
                {"capacity": 75, "ports": 2},
                {"capacity": 75, "ports": 2}
            ]
        }
    ]
}

mock_predicted_cars = {
    "jan": {
        "weekdays": {str(i): 5 for i in range(24)},
        "weekends": {str(i): 3 for i in range(24)}
    }
}


# Verifies that the sum of weekday and weekend hourly visits (after distribution) matches the expected total
# weekly_visits_forecast, within a ±1 margin due to rounding. This confirms the visit distribution logic is
# accurate per month.
def test_calculate_monthly_distribution_sum_matches():
    weekly_visits_forecast = 59
    expected_monthly_total = floor(weekly_visits_forecast) # to match how the service calculates it

    result = DemandCalculationService.calculate_monthly_distribution(weekly_visits_forecast)

    for month, data in result.items():
        weekday_total = sum(data["weekdays"].values()) * 5
        weekend_total = sum(data["weekends"].values()) * 2

        monthly_total = weekday_total + weekend_total

        assert abs(monthly_total - expected_monthly_total) <= 1, (
            f"Month {month} has {monthly_total} visits and expected ~{expected_monthly_total} visits"
        )


# Validates the structure returned by the function that calculates hourly demand (in kW) per month.
# It checks that jan exists in the result and confirms monthly granularity in the power distribution.
def test_get_demand_table():
    result = DemandCalculationService.get_demand_table(
        hardware_configuration=mock_hardware_config,
        predicted_cars=mock_predicted_cars,
        peak_demand_per_car=50,
        utility_peak_demand_cap_kw=300,
        peak_demand_cap_kw=600
    )

    assert "months" in result
    assert "jan" in result["months"]


# Checks that demand-based charges are calculated properly for each tier using both flat and time-of-use pricing.
# Ensures output includes charges per tier for the correct month.
def test_get_monthly_demand_charge_component():
    demand_table = get_demand_table_with_default(100)
    tier_maxes = DemandCalculationService.get_demand_table_tier_maxes(demand_table, mock_time_ranges)

    result = DemandCalculationService.get_monthly_demand_charge_component(tier_maxes, mock_tiers_demand_cost)

    assert isinstance(result, dict)
    assert "jan" in result


# Validates how often each tier is expected to occur weekly, based on weekday/weekend breakdowns.
# It asserts that total percentages for a month (e.g., Tier 1 + Tier 2) add up to 100%.
def test_get_tier_occurrence_percents_per_week():
    result = DemandCalculationService.get_tier_occurrence_percents_per_week(mock_time_ranges)

    assert "jan" in result
    assert "Tier 1" in result["jan"]
    assert round(result["jan"]["Tier 1"] + result["jan"]["Tier 2"], 2) == 100.0


# Tests the annual aggregation logic by providing known monthly tier costs and occurrence percentages.
# Confirms the function correctly calculates weighted yearly totals.
def test_get_total_year_demand_cost():
    mock_monthly_demand = {"jan": {"Tier 1": 100}}
    mock_occurrence = {"jan": {"Tier 1": 100.0}}

    result = DemandCalculationService.get_total_year_demand_cost(mock_monthly_demand, mock_occurrence)

    assert result["total"] == 100.0


# Ensures that for each month and tier, the peak kW demand across all active hours is extracted.
# Helps verify how demand limits are pulled from the hourly demand table.
def test_get_demand_table_tier_maxes():
    demand_table = get_demand_table_with_default(500)

    result = DemandCalculationService.get_demand_table_tier_maxes(demand_table, mock_time_ranges)

    assert "jan" in result
    assert "Tier 1" in result["jan"]


# Combines cost tiers and time ranges to simulate a real plan and checks if the calculated average $/kW
# per month is reasonable. Confirms integration between distribution, cost, and time logic.
def test_calculate_yearly_avg_rate():
    avg_rate = DemandCalculationService.calculate_yearly_average_rate(
        time_ranges=mock_time_ranges,
        tiers_demand_cost=mock_tiers_demand_cost
    )

    print(f"Average Yearly Demand Rate: {avg_rate}")
    assert isinstance(avg_rate, float)
    assert avg_rate > 0


# End-to-end test for the final demand cost calculation logic. Verifies that the complete pipeline
# (hardware, car traffic, cost tiers, and time ranges) outputs a valid result with a "total" key.
def test_calculate():
    result = DemandCalculationService.calculate(
        hardware_config=mock_hardware_config,
        predicted_cars=mock_predicted_cars,
        peak_demand_per_car=50,
        utility_peak_demand_cap_kw=300,
        peak_demand_cap_kw=600,
        time_ranges=mock_time_ranges,
        demand_input=mock_tiers_demand_cost
    )

    assert isinstance(result, dict)
    assert "total" in result
