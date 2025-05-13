import math

from services.energy_consumption_calculation import EnergyConsumptionService
energy_map = {
        "jan":{
            "weekdays": {
                "9" : 522,
                "10": 654,
                "11": 764,
                "12": 898,
                "13": 985,
                "14": 987,
                "15": 964,
                "16": 969,
                "17": 867,
                "18": 741,
                "19": 584,
                "20": 444,
                "21": 406,
            },
            "weekends": {
                "9": 100,
                "10": 186,
                "11": 250,
                "12": 365,
                "13": 487,
                "14": 458,
                "15": 461,
                "16": 400,
                "17": 394,
                "18": 357,
                "19": 306,
                "20": 158,
                "21": 75,
            }
        }
    }
hardware_config = {
        "cabinets": [
            {
                "capacity": 700,
                "chargers": [{"capacity": 600, "ports": 4}, {"capacity": 600, "ports": 4}],
            },            {
                "capacity": 700,
                "chargers": [{"capacity": 600, "ports": 4}],
            }
        ]
    }
expected_car_visits = {
    "jan": {
        "weekdays": {
            "9": 1,
            "10": 2,
            "11": 5,
            "12": 5,
            "13": 7,
            "14": 8,
            "15": 8,
            "16": 10,
            "17": 11,
            "18": 11,
            "19": 9,
            "20": 9,
            "21": 3,
        },
        "weekends": {
            "9": 0,
            "10": 0,
            "11": 1,
            "12": 1,
            "13": 3,
            "14": 4,
            "15": 4,
            "16": 6,
            "17": 7,
            "18": 4,
            "19": 3,
            "20": 2,
            "21": 1,
        }
    }
}
tiers_energy_cost = {
    "low": 0.1,
    "medium": 0.2,
    "high": 0.3,
}
time_ranges = {
    "jan":{
        "weekdays": {
            "low": {"time_ranges": [{"from": 0, "to": 11}]}
        },
        "weekends": {
            "medium": {"time_ranges": [{"from": 0, "to": 23}]},
        }
    }
}

utilization_percent = 80

def test_energy_consumption_table():
    result = EnergyConsumptionService.get_energy_consumption_table(expected_car_visits, hardware_config, utilization_percent)

    assert "energy_consumption_table" in result
    assert "max_serviced_cars_table" in result
    assert "handled_weekly_visitors" in result


def test_calculate_energy_consumption():
    expected_total = 0
    for month in energy_map.values():
        for hours in month.values():
            for value in hours.values():
                expected_total += value

    result = EnergyConsumptionService.calculate_energy_consumption(energy_map)
    assert result == expected_total

def test_calculate_energy_consumption_cost():
    result = EnergyConsumptionService.calculate_energy_consumption_cost(energy_map, tiers_energy_cost, time_ranges)
    assert "total" in result