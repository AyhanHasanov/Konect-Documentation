# NEVI Service

## Overview

The service uses the NEVI API.

The purpose of the service is to determine if a given location is **near a federally designated NEVI EV charging corridor** by:

-   Converting a U.S. state name to its abbreviation.
-   Fetching all NEVI route geometries for the selected state.
-   Checking if the location falls within a given distance (default 5000 meters) of any route path.
    

It is triggered by the controller route:

```python
@ROUTE.route('/api/v1/nevi-proximity', methods=["POST"])
```

## Main Function: `get_nevi_route(lat, lon, state, radius=5000)`

This is the only defined function in the service and the main entry point, called directly from the router.

### Workflow:

-   Converts the state name to its two-letter abbreviation using `state_name_to_abbreviation()` from the utils.
    
-   Calls `fetch_nevi_routes()` to retrieve all NEVI corridor geometries for the state.
    
-   Passes these routes to `check_nevi_proximity_arcgis()` from the api to determine if the location lies within the given radius.
    
-   Returns `True` if a route is nearby, or `False` otherwise.
    

The function encapsulates **proximity validation logic** that supports strategic EV charger placement decisions.

----------

### API Helper Function: `check_nevi_proximity_arcgis(lat, lon, nevi_routes, radius)`

Processes all NEVI routes and determines whether the provided location is close enough to any route.

#### Workflow:

-   Loops through each route and its sub-paths.
    
-   Uses a bounding box filter to quickly identify route points that might be within range.
    
-   Performs accurate geodesic distance checks using `is_in_geodesic()` on filtered candidates.
    
-   Returns `True` immediately if any point is within the defined radius.
    

This function ensures that the check is both **performance-efficient** and **geospatially precise**.
