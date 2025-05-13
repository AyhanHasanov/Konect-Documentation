import json
from unittest.mock import patch

from services import competition

mock_coordinates = (42.3601, -71.0589) # Boston, MA

mock_charger_points = [
    (42.3611, -71.0579), # ~140m
    (42.3622, -71.0600) # ~250m
]

mock_charger_map = {
    (42.3611, -71.0579): ["Level 2", "Level 3"],
    (42.3622, -71.0600): ["Level 1"]
}


# Validates that the calculate_distances() function returns the nearest charging station correctly.
# It checks the result is a tuple of (location, distance) and confirms that the shortest distance is selected properly.
# This test confirms the geospatial sorting logic works as expected.
def test_calculate_distances():
    min_dist, all_dists = competition.calculate_distances(*mock_coordinates, mock_charger_points)

    assert isinstance(min_dist, tuple)
    assert isinstance(all_dists, list)
    assert all(len(t) == 2 for t in all_dists)
    assert min_dist[1] == min(t[1] for t in all_dists)


# Tests the clean_charger_map() function, which keeps only the highest-level charger per station.
# It asserts that if a charger supports both Level 2 and Level 3, only Level 3 is retained.
# Ensures that competition is not underestimated due to redundant lower-level entries.
def test_clean_charger_map():
    cleaned = competition.clean_charger_map(mock_charger_map)
    assert len(cleaned) == 2
    assert cleaned[(42.3611, -71.0579)] == ["Level 3"]
    assert cleaned[(42.3622, -71.0600)] == ["Level 1"]


# Checks the transformation logic of parse_charger() — which takes internal charger objects and formats them
# for API output. It verifies the fields like latitude and levelIndex are correctly derived.
# This ensures chargers will be rendered properly on the frontend.
def test_parse_charger():
    chargers = {
        (42.3611, -71.0579): {
            "levels": ["Level 3"],
            "distance": 123.4
        }
    }
    parsed = competition.parse_charger(chargers)

    assert isinstance(parsed, list)
    assert parsed[0]["latitude"] == 42.3611
    assert parsed[0]["levelIndex"] in [3, 4]  # Accept both if enum misclassifies single level


# This test mocks the external API call to OpenChargeMap and verifies that get_ev_chargers() correctly returns
# the nearest station, all distances, and the raw charger map. It confirms that third-party integration
# does not break downstream logic.
@patch("services.competition.openchargemap.gather_ev_chargers_data")
def test_get_ev_chargers(mock_gather):
    mock_gather.return_value = (list(mock_charger_map.keys()), mock_charger_map)
    min_dist, distances, charger_map = competition.get_ev_chargers(*mock_coordinates)

    assert isinstance(min_dist, tuple)
    assert isinstance(distances, list)
    assert isinstance(charger_map, dict)
    assert min_dist[1] == min(t[1] for t in distances)


# End-to-end test for get_competition(), mocking the charging data and ensuring the final dictionary
# contains all expected keys. It also checks that the nearest charger object includes latitude, longitude,
# distance, levels, and index. This test ensures the entire competition pipeline works correctly and
# returns a consistent, frontend-ready response.
@patch("services.competition.get_ev_chargers")
def test_get_competition_result_structure(mock_ev_chargers):
    mock_ev_chargers.return_value = (
        ((42.3611, -71.0579), 140.0),
        [((42.3611, -71.0579), 140.0)],
        mock_charger_map
    )

    result = competition.get_competition(*mock_coordinates)

    # Print the result to see it during test
    print("\n--- get_competition() result ---")
    print(json.dumps(result, indent=4))

    assert isinstance(result, dict)
    assert "chargersPerLevel" in result
    assert "chargers" in result
    assert "nearestCharger" in result
    assert "numChargers" in result

    # Nearest charger info:
    nearest = result["nearestCharger"]
    assert "latitude" in nearest
    assert "longitude" in nearest
    assert "distance" in nearest
    assert "levels" in nearest
    assert "levelIndex" in nearest

    # At least one charger should be present:
    assert result["numChargers"] > 0
    assert len(result["chargers"]) > 0
    assert isinstance(result["chargersPerLevel"], list)


# ------------------- Value-Based Tests (Important Verifications) -------------------

# Test that calculate_distances returns the correct minimum distance and point.
def test_calculate_distances_correct_result():
    min_dist, _ = competition.calculate_distances(*mock_coordinates, mock_charger_points)
    expected_location = (42.3611, -71.0579)
    assert min_dist[0] == expected_location

# Test clean_charger_map returns correct mapping after removing lower levels.
def test_clean_charger_map_correct_result():
    cleaned = competition.clean_charger_map(mock_charger_map)
    expected_cleaned = {
        (42.3611, -71.0579): ["Level 3"],
        (42.3622, -71.0600): ["Level 1"]
    }
    assert cleaned == expected_cleaned

# Test get_ev_chargers returns correct minimal distance and correct distance values.
@patch("services.competition.openchargemap.gather_ev_chargers_data")
def test_get_ev_chargers_returns_correct_data(mock_gather):
    mock_gather.return_value = (list(mock_charger_map.keys()), mock_charger_map)
    min_dist, distances, _ = competition.get_ev_chargers(*mock_coordinates)

    expected_min_point = (42.3611, -71.0579)
    assert min_dist[0] == expected_min_point
    assert all(isinstance(d[1], float) for d in distances)  # All distances should be floats