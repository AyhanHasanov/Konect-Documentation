from services.energy_consumption_calculation import EnergyConsumptionService, get_energy_cost_per_hour_map

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

mock_expected_car_visits_per_hour = {
    "jan": {
        "weekdays": {str(i): 5 for i in range(24)},
        "weekends": {str(i): 3 for i in range(24)}
    }
}

mock_utilization_percent = 80

mock_time_ranges = {
    "jan": {
        "weekdays": {
            "Tier 1": {"time_ranges": [{"from": 8, "to": 18}], "occurance_percent": 60},
            "Tier 2": {"time_ranges": [{"from": 19, "to": 23}], "occurance_percent": 20},
        },
        "weekends": {
            "Tier 1": {"time_ranges": [{"from": 10, "to": 20}], "occurance_percent": 50},
            "Tier 2": {"time_ranges": [{"from": 21, "to": 23}], "occurance_percent": 30},
        }
    }
}

mock_tiers_energy_cost = {
    "Tier 1": 0.10,
    "Tier 2": 0.20
}


# Tests if the energy consumption table returns expected keys and structure.
def test_get_energy_consumption_table_structure():
    result = EnergyConsumptionService.get_energy_consumption_table(
        expected_car_visits_per_hour=mock_expected_car_visits_per_hour,
        hardware_config=mock_hardware_config,
        utilization_assumption_percent=mock_utilization_percent
    )

    assert "energy_consumption_table" in result
    assert "max_serviced_cars_table" in result
    assert "handled_weekly_visitors" in result
    assert isinstance(result["energy_consumption_table"]["jan"]["weekdays"]["0"], int)


# Verifies the total energy consumption value is a positive integer.
def test_calculate_energy_consumption_total():
    energy_table = EnergyConsumptionService.get_energy_consumption_table(
        expected_car_visits_per_hour=mock_expected_car_visits_per_hour,
        hardware_config=mock_hardware_config,
        utilization_assumption_percent=mock_utilization_percent
    )["energy_consumption_table"]

    total = EnergyConsumptionService.calculate_energy_consumption(energy_table)

    assert isinstance(total, int)
    assert total > 0


# Tests that the hourly cost map contains valid float values for cost calculation.
def test_get_energy_cost_per_hour_map_structure():
    energy_table = EnergyConsumptionService.get_energy_consumption_table(
        expected_car_visits_per_hour=mock_expected_car_visits_per_hour,
        hardware_config=mock_hardware_config,
        utilization_assumption_percent=mock_utilization_percent
    )["energy_consumption_table"]

    result = get_energy_cost_per_hour_map(energy_table, mock_tiers_energy_cost, mock_time_ranges)

    assert "jan" in result
    assert "weekdays" in result["jan"]
    assert isinstance(result["jan"]["weekdays"]["10"], float)


# Verifies the total cost returned is a float and contains a breakdown table.
def test_calculate_energy_consumption_cost_total():
    energy_table = EnergyConsumptionService.get_energy_consumption_table(
        expected_car_visits_per_hour=mock_expected_car_visits_per_hour,
        hardware_config=mock_hardware_config,
        utilization_assumption_percent=mock_utilization_percent
    )["energy_consumption_table"]

    result = EnergyConsumptionService.calculate_energy_consumption_cost(
        energy_consumption_map=energy_table,
        tiers_energy_cost=mock_tiers_energy_cost,
        time_ranges=mock_time_ranges
    )

    assert "total" in result
    assert isinstance(result["total"], float)
    assert result["total"] > 0