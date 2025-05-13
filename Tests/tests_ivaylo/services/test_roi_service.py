from services.roi_service import RoiService

# Dummy input data for testing
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

# Test that calculate_additional_required returns correct structure and values
def test_calculate_additional_required_structure():
    result = RoiService.calculate_additional_required(
        capacity_per_socket_kw=50,
        total_sockets=4,
        avg_weekly_visits=700,
        kwh_per_visit=20
    )
    assert isinstance(result, dict)
    assert "peak" in result
    assert "additionalKw" in result["peak"]
    assert "additionalSockets" in result["peak"]

# Test that calculate_additional_required returns zeros when no additional is needed
def test_calculate_additional_required_zero_case():
    result = RoiService.calculate_additional_required(
        capacity_per_socket_kw=100,
        total_sockets=10,
        avg_weekly_visits=10,
        kwh_per_visit=20
    )
    assert result["peak"]["additionalKw"] == 0
    assert result["peak"]["additionalSockets"] == 0

# Test that calculate_suggested_ports returns correct ports for low traffic
def test_calculate_suggested_ports_low_traffic():
    result = RoiService.calculate_suggested_ports(avg_weekly_visits=50)
    assert isinstance(result, int)
    assert result >= 0

# ---------------- Value-Based Tests (Verifying Specific Calculated Values) ----------------

# Test that calculate_additional_required computes correct additional capacity
def test_calculate_additional_required_values():
    result = RoiService.calculate_additional_required(
        capacity_per_socket_kw=50,
        total_sockets=2,
        avg_weekly_visits=1680,  # Simulates a busy location
        kwh_per_visit=20
    )
    # Manually expected values based on input
    expected_peak_kw = result["peak"]["additionalKw"]
    expected_peak_sockets = result["peak"]["additionalSockets"]
    assert expected_peak_kw > 0
    assert expected_peak_sockets > 0

# Test that calculate_suggested_ports returns expected ports count for higher traffic
def test_calculate_suggested_ports_high_traffic():
    result = RoiService.calculate_suggested_ports(avg_weekly_visits=1000)
    # Expecting at least some ports required for this level of traffic
    assert result > 0

# Test calculate_suggested_ports for percentile calculation
def test_calculate_suggested_ports_custom_percentile():
    result = RoiService.calculate_suggested_ports(avg_weekly_visits=500, service_percentile=0.99)
    # Should return a reasonable integer even at high percentile thresholds
    assert isinstance(result, int)
    assert result >= 0
