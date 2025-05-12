import pandas as pd
from pandas.testing import assert_frame_equal, assert_series_equal
from services.score import normalize, calculate_categories, get_score

def test_normalize_basic():
    s = pd.Series([20, 40, 60])
    expected = pd.Series([0.0, 0.5, 1.0])
    result = normalize(s)
    assert_series_equal(result, expected)

def test_normalize_invert():
    s = pd.Series([20, 40, 60])
    expected = pd.Series([1.0, 0.5, 0.0])
    result = normalize(s, invert=True)
    assert_series_equal(result, expected)

def test_normalize_single_value():
    s = pd.Series([20])
    expected = pd.Series([1])
    result = normalize(s)
    assert_series_equal(result, expected)    


def test_normalize_single_value_invert():
    s = pd.Series([20])
    expected = pd.Series([0])
    result = normalize(s, invert=True)
    assert_series_equal(result, expected)


def test_get_score_end_to_end():
    records = [
        {
            "id": 1,
            "siteName": "Site A",
            "totalPopulation": 10000,
            "medianHouseholdIncome": 55000,
            "perCapitaIncome": 25000,
            "predictedEvRegistrations": 200,
            "level3Chargers": 2,
            "totalChargers": 5,
            "distanceToNearestCharger": 1.0,
            "utilityCostPerKwh": 0.15,
            "revenuePerKwh": 0.3,
            "npv": 10000,
            "averageWeeklyVisits": 150,
            "utilization": 0.7,
            "isOnNeviRoute": 1
        },
        {
            "id": 2,
            "siteName": "Site B",
            "totalPopulation": 5000,
            "medianHouseholdIncome": 45000,
            "perCapitaIncome": 20000,
            "predictedEvRegistrations": 100,
            "level3Chargers": 1,
            "totalChargers": 3,
            "distanceToNearestCharger": 5.0,
            "utilityCostPerKwh": 0.25,
            "revenuePerKwh": 0.25,
            "npv": -5000,
            "averageWeeklyVisits": 100,
            "utilization": 0.4,
            "isOnNeviRoute": 0
        }
    ]

    result_df = get_score(records)

    expected_columns = [
        "siteName",
        "Market_Potential_Score",
        "Charging_Infrastructure_Score",
        "Financial_Utilization_Performance_Score",
        "NEVI_Score",
        "finalScore",
        "id"
    ]
    for col in expected_columns:
        assert col in result_df.columns

    assert result_df["finalScore"].between(0, 100).all()

    assert result_df.set_index("siteName").loc["Site A", "NEVI_Score"] == 0.10
    assert result_df.set_index("siteName").loc["Site B", "NEVI_Score"] == 0.0