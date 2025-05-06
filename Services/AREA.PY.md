# Area

This service provides access to **population data** for a given ZCTA code.
It’s used to estimate **market size** or **user potential** in EV charger ROI calculations.

The service defines two functions - `get_total_population(zcta)` and `get_scoring_columns(zcta)`
`get_total_population` calls `get_scoring_columns` (which returns 3 columns from an outer database) fetching only the first returned column which is the population.

## Function: `get_total_population(zcta)`

1. Receives a **ZCTA** string (e.g., `"90210"`)

2. Looks up the total population for that area using a preloaded dataset or query (e.g., from census data)

3. Returns an **integer** value representing the number of residents in that area.


**Example**:
```python

get_total_population("90210") # → 21002

```

## Error Handling
- If ZCTA is invalid or missing in the source, raises a `TypeError` or `ValueError`

- These are caught by the `roi.py` route and converted to an `ApiException`

  
## This service is used In:

-  `roi.py` to calculate **EV adoption %**, and **project charger demand**

- Any feature that needs demographic info for financial modeling