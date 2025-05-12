from api import openchargemap
import pytest
from services.competition import calculate_distances, get_ev_chargers, get_competition, clean_charger_map, parse_charger

lat     = 42.3601
long    = -71.0589

dummy_points        = [
    (42.3611, -71.0579),
    (42.3591, -71.0599),
    (42.3605, -71.0590)
]

dummy_charger_map   = {
    (42.3611, -71.0579): ["Level 1 : Low (Under 2kW)"],
    (42.3591, -71.0599): ["Level 2 : Medium (Over 2kW)"],
    (42.3605, -71.0590): ["Level 3:  High (Over 40kW)"]
}

dummy_charger_map_mixed = {
    (42.3611, -71.0599): ["Level 1 : Low (Under 2kW)", "Level 3:  High (Over 40kW)"],
    (42.3591, -710599) : ["Level 2 : Medium (Over 2kW)"]
}

def test_calculate_min_distance():
    min_point, all_distances = calculate_distances(lat, long, dummy_points)

    #Find the point with the minimum distance
    expected_min_point = ((float('inf'), float('inf')), float('inf'))
    for d in all_distances:
        if d[1] < expected_min_point[1]:
            expected_min_point = d

    assert min_point == expected_min_point

def test_clean_charger_map():
    result = clean_charger_map(dummy_charger_map_mixed)
    expected = {
        (42.3611, -71.0599): ["Level 3:  High (Over 40kW)"],
        (42.3591, -710599) : ["Level 2 : Medium (Over 2kW)"]
    }

    assert result == expected

def test_parse_charger():
    chargers = {
        (42.3611, -71.0579): {
            "distance": 100,
            "levels":
                [
                    "Level 1 : Low (Under 2kW)",
                    "Level 2 : Medium (Over 2kW)"
                ]
        },
        (42.3605, -71.0590): {
            "distance": 600,
            "levels":
                [
                    "Level 3:  High (Over 40kW)"
                ]
        }
    }

    result = parse_charger(chargers)
    expected = [
        {
            "latitude": 42.3611,
            "longitude": -71.0579,
            "distance": 100,
            "levels": ["Level 1 : Low (Under 2kW)", "Level 2 : Medium (Over 2kW)"],
            "levelIndex": 4
        },
        {
            "latitude": 42.3605,
            "longitude": -71.0590,
            "distance": 600,
            "levels": ["Level 3:  High (Over 40kW)"],
            "levelIndex": 3
        }
    ]

    assert result == expected

def test_get_competition_with_data():
    result = get_competition(lat, long)
    assert "chargersPerLevel" in result
    assert "chargers" in result
    assert "nearestCharger" in result

def test_get_competition_without_data():
    #override mock
    openchargemap.gather_ev_chargers_data = lambda lat, lon: ([], {})

    result = get_competition(lat, long)
    assert result == {
        "chargersPerLevel": [],
        "chargers": [],
        "nearestCharger": None,
        "numChargers": 0
    }