from services.energy_consumption_calculation import EnergyConsumptionService
from services.revenue_calculation import RevenueCalculationService


def test_revenue_calculation_basic():
    utilization = 90
    multiplier = 3

    hardware_config = {
        "cabinets": [
            {
                "capacity": 700,
                "chargers": [{"capacity": 600, "ports": 4}, {"capacity": 600, "ports": 4}],
            },
            {
                "capacity": 700,
                "chargers": [{"capacity": 600, "ports": 4}],
            }
        ]
    }

    expected_visits = {
        "jan": {
            "weekdays": {"13": 45, "14": 33, "15": 12, "16": 23, "17": 12, "18": 23, "19": 22, "20": 12, "21": 12 },
            "weekends": {"13": 15, "14": 20, "15": 18, "16": 16, "17": 16, "18": 10, "19": 8, "20": 8, "21": 10 }
        }
    }

    time_ranges = {
        "jan": {
            "weekdays": {
                "Tier 1": {"time_ranges": [{"from": 0, "to": 14}], "occurrence_percent": 90},
                "Tier 2": {"time_ranges": [{"from": 14, "to": 16}], "occurrence_percent": 90},
                "Tier 3": {"time_ranges": [{"from": 16, "to": 23}], "occurrence_percent": 90},
            },
            "weekends": {
                "Tier 1": {"time_ranges": [{"from": 0, "to": 14}], "occurrence_percent": 90},
                "Tier 2": {"time_ranges": [{"from": 14, "to": 16}], "occurrence_percent": 90},
                "Tier 3": {"time_ranges": [{"from": 16, "to": 23}], "occurrence_percent": 90},
            }
        }
    }

    tier_costs = {
        "Tier 1": 0.11,
        "Tier 2": 0.10,
        "Tier 3": 0.08,
    }

    energy_data = EnergyConsumptionService.get_energy_consumption_table(
        expected_visits, hardware_config, utilization
    ).get("energy_consumption_table")

    #json
    revenue = RevenueCalculationService.calculate(
        energy_data, tier_costs, time_ranges, multiplier
    )

    revenue_jan_weekdays_total = 0
    revenue_jan_weekend_total = 0

    for time, time_value in revenue["table"]["jan"]["weekdays"].items():
        revenue_jan_weekdays_total += time_value

    for time, time_value in revenue["table"]["jan"]["weekends"].items():
        revenue_jan_weekend_total += time_value

    revenue_jan_weekdays_avg = revenue_jan_weekdays_total / len(revenue["table"]["jan"]["weekdays"])
    revenue_jan_weekend_avg = revenue_jan_weekend_total / len(revenue["table"]["jan"]["weekends"])

    assert "jan" in revenue["table"]
    assert "weekdays" in revenue["table"]["jan"]
    assert "weekends" in revenue["table"]["jan"]
    assert revenue_jan_weekdays_total > 0
    assert revenue_jan_weekdays_avg > 0
    assert revenue_jan_weekend_total > 0
    assert revenue_jan_weekend_avg > 0