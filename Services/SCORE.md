# Score Service

## Overview
The service defines 3 functions - `get_score` (main function used by controllers), `calculate_categories` and `normalize`, the latter two being helper functions used by the `get_score`.

This service is used to compute a composite `finalScore` to rank and assess different potential or existing sites based on multiple weighted criteria.

## Main Function: `get_score(records)`:
1. The function accepts a list of dictionaries (records), likely from API input.
2. Converts records to a DataFrame with index siteName.
3. Calls calculate_categories() to populate category scores.
4. Adds a NEVI_Score (from a binary isOnNeviRoute column) × 0.10.
5. Computes a finalScore as the sum of all weighted scores × 100.

6. Returns a new DataFrame containing:
	- Individual scores
	- Final score
	- Site name and ID for reference

## Helper functions
### `calculate_categories(df)`:
Defines **three weighted scoring categories**:

-   Market_Potential (25%)
-   Charging_Infrastructure (20%)
-   Financial_Utilization_Performance (45%)
    

Each category has:

-   A list of relevant columns.
-   Per-column normalization:
    -   Inverted for costs (`utilityCostPerKwh`) since lower is better.
    -   Boosted for `predictedEvRegistrations` (×1.5 weight) indicating higher importance.
    -   NPV: normalized but capped at 0 for negative values.
        

Each category's score is the **mean of its normalized features × weight**.

### `normalize(series, invert=False)`:

This function rescales values in a pandas Series to a range between 0 and 1:

-   If the series has only one value → returns `1` or `0` depending on `invert`.
-   If all values are the same → returns `1` (or `0` if `invert`) since normalization isn't meaningful.
-   `invert=True` → values are reversed (`1 - normalized`) so that _lower is better_.
    
This is used to allow comparison across diverse metrics.