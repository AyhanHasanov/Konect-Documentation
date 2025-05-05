
This document explains the **demand plan parsing logic** in `services/plan_parser.py`.

Its purpose is to **extract and organize EV utility rate plan data** from the OpenEI API response into a structured format used for demand and cost calculations.

---

## Purpose

The service receives raw utility rate plan data and organizes:

- Hourly time ranges per tier for each month

- Monthly flat demand charges

- Time-of-use demand charges

- Energy rate tiers

- Fixed costs


It is triggered by OpenEI API responses and used in:

- `demand.py` route

- `demand_calculation.py` for cost computation


---

## Main Class: `DemandParser(api_call)`

**This is the main interface used throughout the app.**  
It wraps the raw OpenEI API response and provides structured access.

---

### `get_tiers_demand_cost()`

Builds and returns a dictionary of:

- `monthly_demand_charge`: A flat rate for each month based on tiers

- `time_of_use_demand_charge`: Per-tier time-specific demand rates by weekday/weekend


---

### `get_tiers_energy_cost()`

Returns tiered energy costs like:

```json
{
  "Tier 1": 0.065,
  "Tier 2": 0.089
}
```

### `get_fixed_cost()`

Returns annualized fixed cost by multiplying the monthly/weekly rate into a year:

```python
12 * $/month or 365 * $/day
```

### `get_tiers_demand_time_ranges()`

Returns **active hourly time ranges per tier** per month, separated into:

- `"weekdays"`

- `"weekends"`


Includes:

```json
"occurrence_percent": 37.5
```

This is used to for how often a tier is active.

### `get_max_demand()` / `get_min_demand()`

Returns the max/min allowable demand for the plan, defaults to:

- `sys.maxsize` if max is undefined

- `0` if min is missing

---

## Helper Functions (Private)

- `build_monthly_demand_charge()`: Builds the flat monthly rate table

- `build_time_of_use_demand_charge()`: Builds TOU demand table

- `get_weekday_time_demand()`: Converts a weekday schedule array into tiered time ranges with % occurrence

- `process_monthly_demand_charge()`: Handles tiered pricing steps

- `calculate_rate()`: Safely calculates `rate + adj`, with defaults

- `get_demand(...)`: Matches hourly data to a demand rate per tier

## Output Examples

**Monthly Demand Charge Output:**

```json
{
  "jan": [{ "from_kw": 0, "to_kw": 9999, "rate": 4.25 }]
}
```


**Time-of-Use Charge Output:**

```json
{
  "jan": {
    "weekday": { "Tier 1": 2.5, "Tier 2": 3.0 },
    "weekend": { "Tier 1": 1.8 }
  }
}
```


**Time Ranges Output:**

```json
{
  "feb": {
    "weekdays": {
      "Tier 1": {
        "time_ranges": [{ "from": 12, "to": 16 }],
        "occurrence_percent": 33.3
      }
    }
  }
}
```

## Links to Related Docs

- [Router (Controller)](demand_router.md)

- [Demand Calculation Logic](demand_calculation.md)

- [OpenEI API Utilities](api.md)