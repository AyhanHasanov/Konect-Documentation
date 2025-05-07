# Date Util

This document explains the utility file:  **`utils/date.py`**

It is responsible for translating month index values (0–11) into readable **three-letter month abbreviations**.

---

## Purpose

This utility is used during:

- Time-based EV demand tier labeling

- Monthly parsing of OpenEI demand schedules


It ensures consistency when working with demand rate schedules across months.

---

## Function: `get_month_abbreviation(index)`

### Input:

- `index`: An integer between 0 and 11 (inclusive)

### What It Does:

- Converts a numeric index to a **3-letter string abbreviation**:

```python
0  → "jan"  
1  → "feb"  
...  
11 → "dec"
```

- Raises an error if index is **out of bounds**.

### Example:

```python
get_month_abbreviation(0)  # → "jan"
get_month_abbreviation(10) # → "nov"
```

### Error Handling:

Raises a `ValueError` if the input is outside the allowed range:

```text
Index must be in the range 0-11.
```

---

## Used In

- `DemandParser.get_tiers_demand_time_ranges()`

- `DemandParser.build_monthly_demand_charge()`

- `DemandCalculationService.get_demand_table()`