## Purpose

This utility provides **traffic and location lift estimates** for a given (latitude, longitude) location.  
It simulates how much benefit (or “lift”) a charger might gain from being placed at that location.

This is essential for calculating **expected charger usage** and **revenue potential** in ROI simulations.

---

## Function: `run_nodes_lift_service(latitude, longitude)`

### What it does:

1. Receives a location (`latitude`, `longitude`)

2. Makes a call to a **pretrained ML model or data service** (implementation-dependent)

3. Returns a dictionary with:

```python
{
    "node_lift": float, # Lift factor from traffic or geographic features
    "traffic_thirty_miles": int, # Vehicles within 30 miles
    "traffic_seventy_miles": int, # Vehicles within 70 miles
    "traffic_above_seventy": int # Vehicles beyond 70 miles
}
```

These numbers are used to adjust **weekly charger visits**, and inform suggested number of ports.

---

### Example Output:

```python
{
    "node_lift": 240,
    "traffic_thirty_miles": 452,
    "traffic_seventy_miles": 893,
    "traffic_above_seventy": 672
}
```

## Used In:

- `roi.py` → for `node_lift`, `traffic_*` values

- ROI simulations

- Suggested charger capacity planning