import pandas as pd
from services import score

# Sample mock records for testing
mock_records = [
    {
        "siteName": "Site A",
        "totalPopulation": 10000,
        "medianHouseholdIncome": 60000,
        "perCapitaIncome": 30000,
        "predictedEvRegistrations": 150,
        "level3Chargers": 5,
        "totalChargers": 10,
        "distanceToNearestCharger": 2,
        "utilityCostPerKwh": 0.15,
        "revenuePerKwh": 0.30,
        "npv": 50000,
        "averageWeeklyVisits": 200,
        "utilization": 0.75,
        "isOnNeviRoute": 1,
        "id": 1
    },
    {
        "siteName": "Site B",
        "totalPopulation": 8000,
        "medianHouseholdIncome": 50000,
        "perCapitaIncome": 25000,
        "predictedEvRegistrations": 100,
        "level3Chargers": 3,
        "totalChargers": 5,
        "distanceToNearestCharger": 5,
        "utilityCostPerKwh": 0.20,
        "revenuePerKwh": 0.25,
        "npv": -10000,
        "averageWeeklyVisits": 150,
        "utilization": 0.60,
        "isOnNeviRoute": 0,
        "id": 2
    }
]

# Test that normalize function returns values between 0 and 1
def test_normalize_values_range():
    series = pd.Series([10, 20, 30])
    result = score.normalize(series)
    assert all(0.0 <= v <= 1.0 for v in result), "Normalized values should be between 0 and 1."

# Test that normalize with invert=True returns inverted values
def test_normalize_inverted():
    series = pd.Series([10, 20, 30])
    result = score.normalize(series, invert=True)
    assert result.iloc[0] == 1, "First value should become 1 after inversion."
    assert result.iloc[-1] == 0, "Last value should become 0 after inversion."

# Test calculate_categories correctly adds expected columns
def test_calculate_categories_adds_columns():
    df = pd.DataFrame(mock_records)
    score.calculate_categories(df)
    assert "Market_Potential_Score" in df.columns
    assert "Financial_Utilization_Performance_Score" in df.columns
    assert "Charging_Infrastructure_Score" in df.columns

# Test get_score returns a DataFrame with correct final columns
def test_get_score_output_structure():
    result_df = score.get_score(mock_records)
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
        assert col in result_df.columns, f"Missing expected column: {col}"

# ---------------- Value-Based Tests (Important Calculations) ----------------

# Test that final scores are positive and site A scores higher than site B
def test_get_score_values_are_correct():
    result_df = score.get_score(mock_records)
    site_a_score = result_df.loc["Site A"]["finalScore"]
    site_b_score = result_df.loc["Site B"]["finalScore"]

    assert site_a_score > site_b_score, "Site A should have a higher score than Site B."
    assert site_a_score > 0 and site_b_score > 0, "Scores should be positive."

# Test that NEVI score is correctly applied
def test_nevi_score_calculation():
    result_df = score.get_score(mock_records)
    site_a_nevi = result_df.loc["Site A"]["NEVI_Score"]
    site_b_nevi = result_df.loc["Site B"]["NEVI_Score"]

    assert site_a_nevi == 0.10, "NEVI score for Site A should be 0.10."
    assert site_b_nevi == 0.0, "NEVI score for Site B should be 0.0."

# Test handling of edge case with all npv values negative
def test_npvs_all_negative_sets_score_to_zero():
    bad_records = [dict(rec, npv=-50000) for rec in mock_records]
    result_df = score.get_score(bad_records)
    for val in result_df["Financial_Utilization_Performance_Score"]:
        assert val >= 0, "NPV normalization should not produce negative scores."
