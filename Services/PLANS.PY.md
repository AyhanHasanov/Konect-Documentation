# Plans Service

## Purpose

This service fetches a **utility rate plan** for a given location and name, by querying OpenEI.

---

## Main Function: `get_plan(latitude, longitude, plan_name, sector)`

### What it does:

1. Uses `make_openei_request()` to:
    
    - Search for utility rate plans within 20-mile radius of `lat/lon`
    
    - Filters by `sector` (e.g., `residential`, `commercial`)
    
2. Iterates through returned plans to **find a match** with `plan_name`.
    
3. When matched:
    
    - Parses the plan with `DemandParser`
    
    - Builds `hourlyRates` using the average cost across 24 hours
    
    - Returns a dict with:
        
        - `planName`, `planId`
        
        - `hourlyRates`: List of 24 hourly average kWh prices
        

### Output:

```json
{
  "planName": "Some Utility Plan",
  "planId": "abc123",
  "hourlyRates": [0.13, 0.14, ..., 0.17]  // 24 floats
}
```

If not found: returns **None**.

---
### Used In:

- `roi.py` → to generate the **scatter graph**
    
- Any visualization of **hour-by-hour pricing**