import pytest
from services import peak_demand

# Dummy hardware setup used across tests
dummy_hardware_config = {
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

# Test that a Port can be occupied and tracks demand correctly
def test_port_occupy():
    port = peak_demand.Port()
    assert not port.is_occupied

    port.occupy(30)
    assert port.is_occupied
    assert port.required_demand_kw == 30

# Test Charger port assignment and power calculations
def test_charger_occupy_and_power():
    ports = [peak_demand.Port() for _ in range(2)]
    charger = peak_demand.Charger(ports, max_power_kw=100)

    assert charger.have_free_ports()
    charger.occupy_free_port(20)
    assert charger.get_current_power() == 80
    assert charger.get_peak_demand_kw() == 20

# Test Cabinet-level power usage and availability of free ports
def test_cabinet_power_calculations():
    charger1 = peak_demand.Charger([peak_demand.Port()], 50)
    charger2 = peak_demand.Charger([peak_demand.Port()], 50)
    cabinet = peak_demand.Cabinet([charger1, charger2], max_power_kw=100)

    cabinet.occupy_free_port(25)
    assert cabinet.have_free_ports()
    assert cabinet.get_current_power() <= 100
    assert cabinet.get_peak_demand_kw() <= 100

# Test Site-wide plugging behavior and peak demand limit enforcement
def test_site_plug_and_peak_demand():
    charger = peak_demand.Charger([peak_demand.Port(), peak_demand.Port()], 100)
    cabinet = peak_demand.Cabinet([charger], 100)
    site = peak_demand.Site([cabinet], 100)

    site.try_to_plug(2, 30)
    assert site.get_peak_demand_kw() <= 100
    assert site.number_of_ports == 2

# Test conversion from JSON-like hardware config to Cabinet objects
def test_convert_to_cabinet_capacities_structure():
    result = peak_demand.convert_to_cabinet_capacities(dummy_hardware_config)

    assert isinstance(result, list)
    assert isinstance(result[0], peak_demand.Cabinet)
    assert result[0].number_of_ports == 4

# Test full peak demand calculation with a valid number of cars
def test_calculate_peak_demand_result():
    result = peak_demand.PeakDemandCalculationService.calculate(
        hardware_configuration=dummy_hardware_config,
        predicted_cars=4,
        peak_demand_per_car=20,
        utility_peak_demand_cap_kw=150,
        peak_demand_cap_kw=600
    )

    assert isinstance(result, (int, float))
    assert result <= 150

# Test edge case when predicted car visits is zero → should return 0
def test_calculate_peak_demand_zero_case():
    result = peak_demand.PeakDemandCalculationService.calculate(
        hardware_configuration=dummy_hardware_config,
        predicted_cars=0,
        peak_demand_per_car=20,
        utility_peak_demand_cap_kw=150,
        peak_demand_cap_kw=600
    )

    assert result == 0
