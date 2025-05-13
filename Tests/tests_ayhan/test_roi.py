def test_roi(app, client):
    request_payload = {
        "planName": "DG-R Primary (Above 500kW)",
        "planSector": "Commercial",
        "planId": "663d4376ba9c13bee3086c46",
        "projectStartDate": "2024-11-04",
        "latitude": 32.7570324,
        "longitude": -117.1297689,
        "state": "California",
        "operatingCost": 300,
        "incentives": 260000,
        "has30c": True,
        "hasBABA": False,
        "subscriptionFeePerMonth": 0,
        "monthlySoftwareCost": 315,
        "hardwareConfig": [
            {"capacity": 700, "chargers": [{"capacity": 0, "ports": 2}, {"capacity": 0, "ports": 2}, {"capacity": 0, "ports": 2}]},
            {"capacity": 700, "chargers": [{"capacity": 0, "ports": 2}]}
        ],
        "hardwareCost": 1802813,
        "installCost": 1802813,
        "totalSockets": 28,
        "flatFeePerSession": 0,
        "utilityCost": {"type": "tou", "peak": 0.6791, "offPeak": 0.1855, "superOffPeak": 0.1482},
        "driverPriceMultiplier": 4,
        "zip": "92116",
        "kwhPerVisit": 25
    }

    response = client.post('/api/v1/roi', json=request_payload)
    
    assert response.status_code == 200

    response_data = json.loads(response.get_data(as_text=True))

    # Ensure core fields are in the response
    assert "avgWeeklyVisits" in response_data
    assert "cashFlowsPerYear" in response_data
    assert "npv" in response_data

def test_roi_and_npv_service():
    request_data = {
        "predicted_ev_registrations": 1188,
        "plan_id": "539f6c1bec4f024411eca5ad",
        "node_lift": 200,
        "peak_demand_per_car": 100,
        "operating_cost": 315,
        "hardware_cost": 225000,
        "installation_cost": 225000,
        "federal_incentives": 0,
        "thirty_c_incentives": 100000,
        "driver_price_multiplier": 5,
        "discount_rate": 3,
        "hardware_config": {
            "cabinets": [
                {"capacity": 200, "chargers": [{"capacity": 200, "ports": 1}, {"capacity": 200, "ports": 1}]},
                {"capacity": 200, "chargers": [{"capacity": 200, "ports": 1}]}
            ]
        }
    }

    response = RoiService.calculateRoiAndNpv(**request_data)

    # Ensure the response is not None
    assert response is not None

def test_overpass_module():
    response = run_overpass_pipeline(40.9230158, -74.1303192)
    assert response, "No response received from Overpass module"

def test_nodes_lift_service():
    response = run_nodes_lift_service(40.9230158, -74.1303192)
    assert response, "No response received from Node Lift service"

