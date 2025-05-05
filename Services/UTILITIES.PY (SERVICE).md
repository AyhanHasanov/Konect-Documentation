This document explains the logic inside the `utilities.py` service, which is used to retrieve **unique electric utility providers** for a specific sector and location using OpenEI.

---

# Purpose

The service supports the `/api/v1/utilities` endpoint by:

- Sending requests to the **OpenEI API**

- Extracting **utility provider names** from matching rate plans

- Removing duplicates

---

# Function: `get_utilities(latitude, longitude, sector)`

### What it does:

1. Calls `make_openei_request()` to fetch utility rate plans

2. Extracts a list of providers using `get_unique_utility_providers()`

3. Returns:

```python
["Utility A", "Utility B", ...]
```

### Example:

```python
get_utilities(42.123, -71.456, "Commercial")
# → ["Boston Electric Co", "PowerGrid MA"]
```

If no data is returned or providers are not found, returns an empty list.

---
# Helper Function: `get_unique_utility_providers(plans)`

## What it does:

- Iterates through rate plan objects

- Extracts and returns a list of **unique `utility` values**    

## Example:

```python
[
  { "utility": "A" },
  { "utility": "B" },
  { "utility": "A" }
]
```

-> Returns:

```python
["A", "B"]
```

---
# Used In

- `utility.py` router

- Any utility provider listing logic that relies on OpenEI API data
