
This document explains the **competition analysis logic** located in `services/competition.py`.

Its purpose is to analyze **EV charging competition** near a given location by:

- Identifying the **nearest** EV charger.

- Returning a **list of chargers** with distance and level info.

- Calculating the **number of chargers per level**.

It is triggered by the controller route:

```python
@ROUTE.route('/api/v1/competition', methods=["POST"])
```

---

# Purpose

The service performs EV charger analysis based on user-provided coordinates and summarizes:

-  The **closest charging station**
  
-  A **list of stations** with distance + charging levels
  
-  Charger level **distribution stats** (e.g., how many Level 2 vs. Level 3)


It works in coordination with:

- External data from **OpenChargeMap**

- Utilities in `utils/charger_levels.py`
 
- Charger-level mapping enums (see [Utils Doc](../utils/CHARGER_LEVELS.PY))

---

# Main Function: `get_competition(latitude, longitude)`

**This is the main entry point, called directly from the router.**

## Workflow:

1. Calls [`get_ev_chargers()`](#get_ev_chargerslatitude-longitude)  
    → Fetches nearby charger coordinates and level data.

2. Filters and cleans data using [`clean_charger_map()`](#clean_charger_mapcharger_map)  
    → Keeps only the **strongest charger per station**.

3. Builds and returns a final JSON response that includes:

	-  `nearestCharger` — closest location with charger level index
	
	-  `chargers` — structured list of chargers
	
	-  `chargersPerLevel` — count per level (Level 1, 2, 3, or MULTIPLE)
	
	-  `numChargers` — total stations after cleaning

---

#  Helper Function: `get_ev_chargers(latitude, longitude)`

##  Purpose:
Fetches raw charging station data using the OpenChargeMap API and processes it.

##  How:

-  Calls [`gather_ev_chargers_data()`](api.md#gather_ev_chargers_datalat-lon-radius_km5)  
    → Gets:
    
    - A list of charger coordinates
    
    - A map of levels per charger

- Uses [`calculate_distances()`](#calculate_distanceslat-lon-points) to:
    
    - Get real-world distance to each charger
    
    - Find the **closest station**

##  Returns:

- `min_distance`: Tuple of (coordinates, meters)

- `distances`: List of all chargers with distance
   
- `charger_map`: Dictionary mapping coordinates → list of charger levels

---

#  Utility: `calculate_distances(lat, lon, points)`

Uses `geopy.geodesic` to measure distances (in meters) from input coordinates to all known charger points.

##  Returns:

-  Closest charger (shortest distance) coordinates and distance in meters
  
-  A list with all close chargers coordinates and other info

---

# Utility: `clean_charger_map(charger_map)`

Ensures **each station is represented by its highest-level charger**.

## Example:

If a given charger support different power level chargers:

```python
["Level 1", "Level 2", "Level 3"]
```

-> We only keep:

```python
["Level 3"]
```

##  Why:

That way we avoid double-counting, prevent underestimating of strong competition and keep the data relevant!

---

#  Formatter: `parse_charger(chargers)`

Prepares each charger entry for frontend or client apps.

Each charger object has a structure like:

```json
{
  "latitude": 42.123,
  "longitude": -71.456,
  "distance": 320.5,
  "levels": ["Level 3"],
  "levelIndex": 3
}
```

Before we build the JSON objects we call **levels_to_index()**  to attach a numeric index to the charger level list.

---

# Links to Related Docs

- [Router (Controller)](competition_router.md)

- [Utils (Level Indexing)](utils.md)

- [External API Call Logic](api.md)