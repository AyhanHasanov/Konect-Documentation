
This document explains the logic in:  **`utils/data.py`**

It provides a fallback **empty schedule matrix** used when OpenEI schedule data is missing or invalid.

---

## Purpose

Many utility rate plans provide **hour-by-hour demand tiers** per day of the week and per month.

If the OpenEI API fails to provide valid data, we fall back on this **default 12x24 schedule**, where:

- **12 rows = months**

- **24 columns = hours in the day**

- All values are set to **0**

---

## Function: `get_empty_schedule()`

### What It Returns:

A **12x24 list of zeros**, representing:

- 12 months

- Each month having 24 hours initialized with `0`

### Example Output:

```python
[
  [0, 0, 0, ..., 0],  # 24 zeros for January
  ...
  [0, 0, 0, ..., 0],  # 24 zeros for December
]
```

### Why It Matters

- Prevents app crashes if a utility plan lacks `demandweekdayschedule`, `demandweekendschedule`, etc.

- Ensures consistent matrix-based operations downstream.   

---

## Used In

- `DemandParser.get_demand_weekday()`

- `DemandParser.get_energy_weekday()`

- `DemandParser.get_demand_weekend()`

- `DemandParser.get_energy_weekend()`