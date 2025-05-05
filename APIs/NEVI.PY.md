This document explains the logic inside the file:  **`api/nevi.py`**

Its job is to determine **if a given location is near a federally designated NEVI highway route**, using GIS path data from ArcGIS.

---

# Purpose

This module supports the **ROI simulation pipeline** by answering:

> **"Is this EV charger location near a NEVI highway?"**

Knowing this helps determine **funding eligibility** and **placement strategy**.

It does so by:

- Fetching NEVI route geometries for a given U.S. state

- Comparing the user’s location to those routes

- Calculating **proximity using geodesic distance**

---

# Function: `check_nevi_proximity_arcgis(lat, lon, nevi_routes, radius)`

## Input:

- `lat`, `lon`: Latitude and longitude of the EV charger

- `nevi_routes`: List of NEVI route geometries (fetched via ArcGIS)

- `radius`: Proximity threshold (in meters)

## What It Does:

1. Iterates through **each NEVI route** and its individual **geometry paths**
    
2. Converts each path into a NumPy array of coordinates
    
3. Applies a **quick box filter** to reduce unnecessary geodesic checks:
    
    - Converts `radius` into an approximate **degree-based distance**
    
    - Uses NumPy to check if any points are **within the bounding box**
    
4. For filtered candidates, calls `is_in_geodesic()`:  
    → Uses precise **geodesic distance** between charger and route
    
5. Returns:
    
    - `True` if **any route** is within the radius
    
    - `False` otherwise
    

---

# Function: `is_in_geodesic(lat, lon, radius, close_points)`

### Purpose:

Checks if any points in `close_points` (from NEVI paths) are within the desired radius of the target point.

## What It Does:

- Loops through filtered NEVI points
    
- Calculates **geodesic distance** to target
    
- Returns `True` on first match
    

This ensures high **geographic precision**.

---

# Function: `fetch_nevi_routes(state)`

## Input:

- `state`: Full name of a U.S. state (e.g. `"Colorado"`)


## What It Does:

1. Builds a query to the **ArcGIS API** using the given state:

```bash
https://services.arcgis.com/xOi1kZaI0eWDREZv/.../FeatureServer/0/query
```

2.  Requests **route features** using `where=STATE='XYZ'`

3. Returns:

```python
data.get("features", [])
```

Which is a list of NEVI route geometries for the specified state.

## Output Example

The proximity check returns a Boolean:

```python
True  # Location is within NEVI radius
False # Not close enough
```

# Used In

- [`process_is_on_nevi_road()` in `roi.py`](roi_router.md#process_is_on_nevi_road)

- NEVI-based **ROI logic**, **funding analysis**, and **visual map markers**