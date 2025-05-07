This document explains the logic inside the utility file:  
**`utils/fetch_overpass_data.py`**

It is used during **traffic density modeling and charger ROI prediction**, by retrieving and analyzing road node activity around a given location via the **OpenStreetMap Overpass API**.

---

# Purpose

This utility supports charger demand modeling by estimating **traffic node behavior** in the area:

- Fetches **road nodes** from OpenStreetMap within a specified radius

- Classifies those nodes as **start**, **stop**, or **passed-through**

- **Bins** them by distance to help model **regional activity patterns**


The output helps train or power ML models that estimate **weekly visits** and **potential lift** for chargers installed at the target coordinates.

# Function: `fetch_overpass_data(lat, lon, radius_km)`

Sends a GET request to the Overpass API and fetches road-related nodes (motorway, trunk, primary) within the radius around the given latitude and longitude.

## Logic:

- Tries up to **4 times** with backoff if the request fails

- Returns parsed JSON of node results, or `None` on failure


## Example:

```python
data = fetch_overpass_data(42.123, -71.456, 250)
```

# Function: `process_nodes(data, target_lat, target_lon, small_radius_km, start_date, end_date)`

Parses the Overpass API result into **three categories** based on distance and timestamp:

- **Start nodes**: Far from the center and within the date window

- **Stop nodes**: Close to the center and within the date window

- **Passed-through**: Appear in both start and stop timestamps


Returns 3 lists of `(lat, lon, timestamp)` tuples.

---

# Function: `bin_nodes_by_distance(nodes, target_lat, target_lon, bin_size_km=10)`

Divides the node list into **distance bins** from the center (e.g., 0–10 km, 10–20 km).

## Output:

- A `Counter` object where keys = bin range (e.g. `0`, `10`)

- Values = number of nodes in that range

---

# Function: `process_location(row, ...)`

Wrapper for one (latitude, longitude) pair stored in a row:

- Calls Overpass

- Runs node classification

- Bins all nodes

- Returns a **dictionary** summarizing node counts in each bin

---

# Function: `run_overpass_pipeline(latitude, longitude, bin_miles=True)`

Full end-to-end utility for generating Overpass-based node stats for a single location:

1. Fetches nodes from Overpass

2. Processes and bins them

3. Outputs a single-row `DataFrame`

4. Optionally converts km bins to **miles**


# Used In:

- [`run_nodes_lift_service()` in `node_lifts_calculations.py`](node_lifts_calculations.md)

- Node-based **weekly visit estimations** and **clustering models**

- Input for ML-based **EV charger profitability simulations**