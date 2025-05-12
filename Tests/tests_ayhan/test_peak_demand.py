from services.peak_demand import Port, Charger, Cabinet, Site
from services.peak_demand import PeakDemandCalculationService


def test_occupy_port():
    port = Port()
    port.occupy(20)
    assert port.is_occupied == True

def test_occupy_charger():
    ports = [Port(), Port(), Port(), Port()]
    charger = Charger(ports, 150)

    assert charger.have_free_ports() == True

    for i in range(1, 5, 1):
        charger.occupy_free_port(20)
        if i != 4:
            assert charger.have_free_ports() == True
        if i == 4:
            assert charger.have_free_ports() == False

    assert charger.get_current_power() == 70

    assert charger.get_peak_demand_kw() == 80


def test_cabinet_occupy_and_demand():
    chargers = [
        Charger([Port(), Port()], 100),
        Charger([Port(), Port()], 100)
    ]
    cabinet = Cabinet(chargers, 180)

    assert cabinet.have_free_ports() == True

    cabinet.occupy_free_port(30)
    cabinet.occupy_free_port(30)
    cabinet.occupy_free_port(30)

    assert cabinet.have_free_ports() == True
    cabinet.occupy_free_port(30)

    assert cabinet.have_free_ports() == False
    assert cabinet.get_peak_demand_kw() == 120
    assert cabinet.get_current_power() == 60  # 180 - 4*30

def test_site_try_to_plug_and_demand():
    #Case:
    #One site with 1 Cabinet with max_power_kw 200
    #The Cabinet has 2 Chargers with max_power_kw 100
    #Each Charger has 2 Ports
    chargers = [
        Charger([Port(), Port()], 100),
        Charger([Port(), Port()], 100)
    ]
    cabinets = [Cabinet(chargers, 200)]
    site = Site(cabinets, 500)

    assert site.get_optimal_cabinet() is not None

    site.try_to_plug(3, 40)  # 4 cars, 40kW each

    assert site.get_peak_demand_kw() == 120

    site.try_to_plug(1, 30)
    assert site.get_peak_demand_kw() == 150

    try:
        site.try_to_plug(1, 40)
    except Exception:
        pass


def test_peak_demand_calculation_normal():
    hardware = {
        "cabinets": [
            {
                "capacity": 200,
                "chargers": [
                    {"capacity": 100, "ports": 2},
                    {"capacity": 100, "ports": 2}
                ]
            }
        ]
    }

    # 3 cars at 50kW each, total 150kW, below utility/site caps
    peak_kw = PeakDemandCalculationService.calculate(
        hardware_configuration=hardware,
        predicted_cars=3,
        peak_demand_per_car=50,
        utility_peak_demand_cap_kw=200,
        peak_demand_cap_kw=600
    )

    assert peak_kw == 150

def test_peak_demand_caps_respected():
    hardware = {
        "cabinets": [
            {
                "capacity": 200,
                "chargers": [
                    {"capacity": 100, "ports": 2},
                    {"capacity": 100, "ports": 2}
                ]
            }
        ]
    }

    peak_kw = PeakDemandCalculationService.calculate(
        hardware_configuration=hardware,
        predicted_cars=4,
        peak_demand_per_car=80,
        utility_peak_demand_cap_kw=200,
        peak_demand_cap_kw=180 
    )

    assert peak_kw == 180

def test_zero_cars_returns_zero():
    hardware = {
        "cabinets": []
    }

    peak_kw = PeakDemandCalculationService.calculate(
        hardware_configuration=hardware,
        predicted_cars=0,
        peak_demand_per_car=50,
        utility_peak_demand_cap_kw=100
    )

    assert peak_kw == 0
