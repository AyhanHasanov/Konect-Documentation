from services.plan_parser import DemandParser

# Dummy API call object simulating OpenEI API response
mock_api_response = {
    "flatdemandstructure": [
        [{"max": 100, "rate": 5}]  # For each month
    ] * 12,
    "energyratestructure": [
        [{"rate": 0.1, "adj": 0.05}],
        [{"rate": 0.2, "adj": 0.0}]
    ] * 6,  # Total 12 months of data
    "demandweekdayschedule": [[0] * 24] * 12,
    "demandweekendschedule": [[0] * 24] * 12,
    "energyweekdayschedule": [[0] * 24] * 12,
    "energyweekendschedule": [[0] * 24] * 12,
    "fixedchargefirstmeter": 10,
    "fixedchargeunits": "$/month",
    "peakkwcapacitymax": 500,
    "peakkwcapacitymin": 100
}

parser = DemandParser(mock_api_response)

# Tests weekday demand schedule retrieval returns a list.
def test_get_demand_weekday():
    result = parser.get_demand_weekday()
    assert isinstance(result, list)

# Tests weekday energy schedule retrieval returns a list.
def test_get_energy_weekday():
    result = parser.get_energy_weekday()
    assert isinstance(result, list)

# Tests weekend demand schedule retrieval returns a list.
def test_get_demand_weekend():
    result = parser.get_demand_weekend()
    assert isinstance(result, list)

# Tests weekend energy schedule retrieval returns a list.
def test_get_energy_weekend():
    result = parser.get_energy_weekend()
    assert isinstance(result, list)

# Tests flat demand structure retrieval and validates length.
def test_get_flat_demand_structure():
    result = parser.get_flat_demand_structure()
    assert isinstance(result, list)
    assert len(result) == 12

# Tests flat month structure returns a list of length 12.
def test_get_flat_month_structure():
    result = parser.get_flat_month_structure()
    assert len(result) == 12

# Tests demand rate structure retrieval (may return None in mock).
def test_get_demand_structure():
    result = parser.get_demand_structure()
    assert result is None or isinstance(result, list)

# Tests energy rate structure retrieval returns a list.
def test_get_energy_structure():
    result = parser.get_energy_structure()
    assert isinstance(result, list)

# Tests retrieval of maximum demand value.
def test_get_max_demand():
    result = parser.get_max_demand()
    assert result == 500

# Tests retrieval of minimum demand value.
def test_get_min_demand():
    result = parser.get_min_demand()
    assert result == 100

# Tests calculation of demand cost tiers including monthly and time-of-use charges.
def test_get_tiers_demand_cost():
    result = parser.get_tiers_demand_cost()
    assert isinstance(result, dict)
    assert "monthly_demand_charge" in result
    assert "time_of_use_demand_charge" in result

# Tests calculation of energy cost tiers and verifies correct value type.
def test_get_tiers_energy_cost():
    result = parser.get_tiers_energy_cost()
    assert isinstance(result, dict)
    assert "Tier 1" in result
    assert isinstance(result["Tier 1"], float)

# Tests fixed cost calculation based on fixed charge and billing cycle.
def test_get_fixed_cost():
    result = parser.get_fixed_cost()
    assert result == 120  # 10 * 12 months

# Tests retrieval of demand time ranges and validates basic structure.
def test_get_tiers_demand_time_ranges():
    result = parser.get_tiers_demand_time_ranges()
    assert "jan" in result
    assert "weekdays" in result["jan"]
    assert isinstance(result["jan"]["weekdays"], dict)

# Tests retrieval of energy time ranges and validates basic structure.
def test_get_tiers_energy_time_ranges():
    result = parser.get_tiers_energy_time_ranges()
    assert "jan" in result
    assert "weekdays" in result["jan"]
    assert isinstance(result["jan"]["weekdays"], dict)


# ---------------- Value-Based Tests (Important Numerical Verifications) ----------------

# Tests that build_monthly_demand_charge returns correct structured data.
def test_build_monthly_demand_charge_returns_valid_structure():
    result = parser.build_monthly_demand_charge()
    assert "jan" in result
    january_charge = result["jan"]
    assert isinstance(january_charge, list)
    assert "from_kw" in january_charge[0]
    assert "to_kw" in january_charge[0]
    assert "rate" in january_charge[0]
    assert january_charge[0]["rate"] == 5


# Tests that get_weekday_time_demand correctly calculates time ranges.
def test_get_weekday_time_demand_returns_correct_structure():
    # Mock a simple time frame collection where Tier 1 is from 0-11 and Tier 2 is from 12-23
    time_frame_collection = [0] * 12 + [1] * 12
    result = parser.get_weekday_time_demand(time_frame_collection)

    assert "Tier 1" in result
    assert "Tier 2" in result
    assert result["Tier 1"]["time_ranges"][0]["from"] == 0
    assert result["Tier 1"]["time_ranges"][0]["to"] == 11
    assert result["Tier 2"]["time_ranges"][0]["from"] == 12
    assert result["Tier 2"]["time_ranges"][0]["to"] == 23


# Tests that get_fixed_cost handles unexpected units gracefully.
def test_get_fixed_cost_with_unexpected_unit():
    bad_api_response = mock_api_response.copy()
    bad_api_response["fixedchargeunits"] = "$/unknown"
    bad_parser = DemandParser(bad_api_response)

    result = bad_parser.get_fixed_cost()
    assert result == 0  # Unknown units should return 0


# Tests calculate_rate correctly handles missing fields.
def test_calculate_rate_with_missing_fields():
    rate_element = {}  # Missing all fields
    result = parser.calculate_rate(rate_element)

    assert result["max_kw"] > 0  # Defaults to sys.maxsize
    assert result["rate"] == 0
    assert result["adj"] == 0


# Tests build_time_of_use_demand_charge returns valid time-based structure.
def test_build_time_of_use_demand_charge_structure():
    result = parser.build_time_of_use_demand_charge()
    assert "jan" in result
    assert "weekday" in result["jan"]
    assert "weekend" in result["jan"]
    assert "Tier 1" in result["jan"]["weekday"]

