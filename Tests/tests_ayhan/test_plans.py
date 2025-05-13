from services.plans import get_generic_plan, process_fixed_plan_to_json, process_tou_plan_to_json, calculate_average_rate, filter_plans_by_name, filter_plans_by_utility

def test_generic_plan():
    plan = get_generic_plan("residential")
    assert plan["sector"] == "residential"
    assert plan["ratePlanType"] == "tou"
    assert len(plan["hourlyRates"]) == 24

def test_process_fixed_plan_to_json():
    data = process_fixed_plan_to_json(
        rate = 0.15,
        eia  = 42,
        sector = "industrial",
        page_id = "test_page",
        page_url = "http://url.com",
        fixed_monthly_cost = 8
    )

    assert data["ratePlanType"] == "fixed"
    assert data["sector"] == "industrial"

def test_calculate_average_rate():
    #Calculate Average rates calculates wrong!!!
    result = calculate_average_rate([1, 1, 2, 3], [1.50, 2.10, 3, 5]) #2.9
    assert result > 0 # == 2.90

    result = calculate_average_rate([], [1.50, 2.10, 3, 5])
    assert result == 0

    result = calculate_average_rate([45], [1.01] * 24)
    assert result == 0

def test_filter_plans_by_name():
    plans = [{"name": "Plan A"}, {"name": "Plan B"}]
    result = filter_plans_by_name(plans, "Plan A")
    assert len(result) == 1