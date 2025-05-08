# Open Charge Map

is document explains the logic inside the file: **`api/openchargemap.py`**

Its job is to connect to the **OpenChargeMap API** and fetch EV charging station data for a given location.

---
##  Purpose

We use OpenChargeMap to:

- Retrieve **up to 100** EV charging stations within a certain radius of given coordinates.    
- Extract:
  
    - Station coordinates
    
    - Charging **level types** (e.g. Level 2, Level 3)
    
- Format data into:
    
    - A list of station coordinates
    
    - A **map** of charging levels by station
    

This API is called by the [`get_ev_chargers()`](competition_service.md#get_ev_chargerslatitude-longitude) function in the **competition service**.

---
##  Function: `gather_ev_chargers_data(lat, lon, radius_km=5)`

### Input:

- `lat`: Latitude of the user's location

- `lon`: Longitude of the user's location

- `radius_km`: Search radius (default = 5km)
  
### What It Does (Step-by-Step):

1. Sends a **GET request** to:
  
```bash
https://api.openchargemap.io/v3/poi
```

Using the passed query parameters it:

2. Parses the JSON response to extract: 

	-  `Latitude` and `Longitude` from `AddressInfo`
	
	-  `Level` information from `Connections`

3. Builds:

	- `locations`: List of coordinates
	    
	- `charger_map`: Dictionary with keys = (lat, lon), values = list of level titles

---
### Output:

The function returns the tuple from the build list and dictionary -> (location, charger_map)

### Example Output:

```python
{
  (42.123, -71.456): ["Level 2 : Medium", "Level 3: High"]
}
```

---
### Error Handling:

If the API returns **HTTP 500**, we raise a custom `ApiException`.

That way we ensure the Spring App or the Frontend can handle the failure.

---

##  Filtering Logic

- Only stations with **valid connections** are included.

- Each level string is stored **uniquely per location** — no duplicates.

- If `"Level"` info is **missing**, we **skip** the connection and log a warning.

---

## Used In

- [`get_ev_chargers()`](competition_service.md#get_ev_chargerslatitude-longitude)

- Indirectly used by the controller: [`@ROUTE('/api/v1/competition')`](competition_router.md#1-router-controller)

