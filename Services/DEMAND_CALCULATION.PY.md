# Demand Calculation Service

This document explains the **EV charger demand cost estimation logic** in `services/demand_calculation.py`.

It converts site usage predictions into **monthly and yearly cost estimates** based on:

- Visitor forecasts

- Utility rate plan tiers

- Charger configurations

---

## Purpose

This service simulates how predicted EV charger usage spreads across:

- Weekdays vs. weekends

- Hours of the day

- Tiers in the utility rate plan


And then it:

- Calculates **hourly and monthly peak demand**

- Matches usage to demand pricing

- Returns **monthly + total yearly cost estimates**


---

## Main Class: `DemandCalculationService`

---

### `calculate_monthly_distribution(weekly_visits_forecast)`

Breaks down weekly site visits into **hourly demand proportions**:

- Weekdays (5-day) vs. weekends (2-day)

- Applies **weighted proportions** for each hour

- Ensures leftover visitors (due to rounding) are redistributed sensibly

- Returns:

```json
{
  "jan": {
    "weekdays": { "11": 9, "12": 7, ... },
    "weekends": { "13": 6, ... }
  },
  ...
}
```

### `get_demand_table(...)`

Returns hourly **peak demand in kW** for all months, using:

- Hardware config

- Demand per car

- Visitor forecast

Uses `PeakDemandCalculationService.calculate(...)` for each hour.

---

### `get_demand_table_tier_maxes(...)`

From the demand table + time ranges, returns **maximum demand per tier** for each month:

```json
{
  "jan": {
    "Tier 1": 25.3,
    "Tier 2": 42.7
  }
}
```

### `get_monthly_demand_charge_component(...)`

Returns **monthly charge per tier**, based on:

- Flat demand charge tiers

- TOU tier pricing

- Peak demand by tier

---

### `get_tier_occurrence_percents_per_week(...)`

Returns **weighted percentage** of how often each tier is used weekly:

```json
{
  "jan": {
    "Tier 1": 55.7,
    "Tier 2": 44.3
  }
}
```

### `get_total_year_demand_cost(...)`

Combines monthly charges + tier weights into a **final yearly cost estimate**:

```json
{
  "total": 3584.74,
  "table": {
    "jan": 312.24,
    ...
  }
}
```

### `calculate_yearly_average_rate(...)`

Returns the **blended $/kW rate** based on a default usage of 500 kW per month:

```python
= total_cost / (12 * 500)
```

### `calculate(...)`

Orchestrates the full process:

1. Generate demand table

2. Get peak per tier

3. Compute tier costs

4. Apply tier occurrence weights

5. Return:


```json
{
  "total": 3990.75,
  "table": {
    "feb": 320.42,
    ...
  }
}
```


---

## 🧰 Helpers

### `get_month_data(month_name, predicted_cars)`

Returns forecasted visits per hour. If missing, uses default 0s.

---

### `get_demand_table_with_default(demand=500)`

Returns a dummy peak demand table assuming 500 kW usage every hour.

Used for estimating **yearly average price** when no real data exists.

---

## Links to Related Docs

- [Router (Controller)](demand_router.md)

- [Plan Parsing Logic](plan_parser.md)

- [EV Peak Demand Model](peak_demand.md)

- [OpenEI API Utils](api.md)