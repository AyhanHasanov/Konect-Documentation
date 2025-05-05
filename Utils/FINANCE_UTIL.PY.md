## Purpose

This utility provides **financial helper functions** used across ROI and demand calculations.  
It ensures consistent modeling of energy usage across time (e.g. hourly proportions) and charger behavior.

---

## Function: `get_hourly_proportions()`

### What it does:

- Returns a list of **24 proportions** — one for each hour of the day.    

Each value represents the **normalized share of daily EV usage** expected in that hour, based on behavioral models.

### Example output:

```python
[0.01, 0.005, ..., 0.08, 0.07]  # 24 values summing to 1.0
```

### Used to:

- Split daily demand into hours

- Weight demand-related costs (e.g., demand charge distributions)

## Function: `predict_visits_by_hour(daily_visits)`

### What it does:

- Given an expected number of daily EV charger visits (e.g. 100),

- Multiplies each by the hourly proportion,

- Returns a list of **predicted hourly visit counts**.

### Example:

```python
predict_visits_by_hour(100)
→ [1.3, 0.7, ..., 8.2, 9.1]  # visits for each hour\
```

## Used In:

- `roi.py` → `process_hourly_demand()`

- Demand-based cash flow modeling

- Cost and utilization estimates per hour