from services.finance_util import get_hourly_proportions, predict_visits_by_hour

def test_get_hourly_proportions_sum_to_one():
    proportions = get_hourly_proportions()
    total = proportions.sum()
    assert abs(total - 1.0) < 0.000001

def test_get_hourly_proportions_has_24_entries():
    proportions = get_hourly_proportions()
    assert len(proportions) == 24

def test_predict_visits_by_hour_total_matches_weekly():
    #Predicted visits should total to the weekly input
    weekly_visits = 7000
    predictions = predict_visits_by_hour(weekly_visits)
    assert len(predictions) == 24
    total_predicted = sum(predictions)
    assert abs(total_predicted - weekly_visits) < 0.000001

def test_predict_visits_by_hour_distribution_shape():
    #Midday > early morning
    weekly_visits = 2400
    predictions = predict_visits_by_hour(weekly_visits)
    assert predictions[12] > predictions[3]
