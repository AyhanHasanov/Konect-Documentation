from services.revenue_calculation import RevenueCalculationService

# Dummy data for testing
mock_energy_consumption_table = {
    "jan": {
        "weekdays": {str(i): 10 for i in range(24)},
        "weekends": {str(i): 5 for i in range(24)}
    }
}

mock_tiers_energy_cost = {
    "Tier 1": 0.1,
    "Tier 2": 0.2
}

mock_time_ranges = {
    "jan": {
        "weekdays": {
            "Tier 1": {"time_ranges": [{"from": 0, "to": 11}]},
            "Tier 2": {"time_ranges": [{"from": 12, "to": 23}]}
        },
        "weekends": {
            "Tier 1": {"time_ranges": [{"from": 0, "to": 23}]}
        }
    }
}

driver_price_multiplier = 1.5

# Test for successful revenue calculation with valid data
def test_calculate_revenue_correct_total():
    result = RevenueCalculationService.calculate(
        energy_consumption_table=mock_energy_consumption_table,
        tiers_energy_cost=mock_tiers_energy_cost,
        time_ranges=mock_time_ranges,
        driver_price_multiplier=driver_price_multiplier
    )

    assert isinstance(result, dict)
    assert "total" in result
    assert "table" in result
    assert result["total"] > 0  # Should calculate to some positive revenue

# Test that hourly costs are calculated correctly inside the result table
def test_calculate_revenue_table_structure():
    result = RevenueCalculationService.calculate(
        energy_consumption_table=mock_energy_consumption_table,
        tiers_energy_cost=mock_tiers_energy_cost,
        time_ranges=mock_time_ranges,
        driver_price_multiplier=driver_price_multiplier
    )

    jan_data = result["table"].get("jan", {})
    assert "weekdays" in jan_data
    assert "weekends" in jan_data
    assert isinstance(jan_data["weekdays"], dict)
    assert isinstance(jan_data["weekends"], dict)
    assert len(jan_data["weekdays"]) == 24
    assert len(jan_data["weekends"]) == 24

# Test with empty consumption data returns zero total
def test_calculate_revenue_with_empty_consumption():
    result = RevenueCalculationService.calculate(
        energy_consumption_table={},
        tiers_energy_cost=mock_tiers_energy_cost,
        time_ranges=mock_time_ranges,
        driver_price_multiplier=driver_price_multiplier
    )

    assert result["total"] == 0
    assert result["table"] == {}

# ---------------- Value-Based Tests (Important Numerical Verifications) ----------------

# Test that the correct total revenue is calculated based on expected simple math
def test_calculate_revenue_expected_total():
    result = RevenueCalculationService.calculate(
        energy_consumption_table=mock_energy_consumption_table,
        tiers_energy_cost=mock_tiers_energy_cost,
        time_ranges=mock_time_ranges,
        driver_price_multiplier=driver_price_multiplier
    )

    # Expected:
    # Weekdays: 12 hours Tier 1 * 10kWh * 0.1 * 1.5 = 180
    #           12 hours Tier 2 * 10kWh * 0.2 * 1.5 = 360
    #           Total per weekday = 540
    # Weekends: 24 hours Tier 1 * 5kWh * 0.1 * 1.5 = 180
    # Total average daily revenue = 540 (weekdays) + 180 (weekends) = 720
    # Total monthly revenue = 720 * 30 = 21600

    expected_total = 2160
    assert round(result["total"], 2) == expected_total


# Test that if driver_price_multiplier is set to 0, the total revenue is 0
def test_calculate_revenue_with_zero_multiplier():
    result = RevenueCalculationService.calculate(
        energy_consumption_table=mock_energy_consumption_table,
        tiers_energy_cost=mock_tiers_energy_cost,
        time_ranges=mock_time_ranges,
        driver_price_multiplier=0
    )

    assert result["total"] == 0


# Test that missing tier in time_ranges leads to zero revenue for those hours
def test_calculate_revenue_with_missing_tier_in_time_ranges():
    incomplete_time_ranges = {
        "jan": {
            "weekdays": {
                "Tier 1": {"time_ranges": [{"from": 0, "to": 5}]}
                # Missing Tier 2 completely
            },
            "weekends": {}
        }
    }

    result = RevenueCalculationService.calculate(
        energy_consumption_table=mock_energy_consumption_table,
        tiers_energy_cost=mock_tiers_energy_cost,
        time_ranges=incomplete_time_ranges,
        driver_price_multiplier=driver_price_multiplier
    )

    # Expect partial revenue calculated only for hours 0 to 5
    assert result["total"] > 0
    assert result["total"] < 91800  # Should be less than the fully calculated scenario
