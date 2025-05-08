# State to Abbrev Util

## Purpose

This utility maps U.S. **state names to their two-letter abbreviations**.

It’s used for:

- Converting `"California"` to `"CA"`

- Fetching state-specific data (e.g., NEVI route maps)

---

## Function: `get_state_abbreviation(state_name)`

### Input:

- `state_name`: Full U.S. state name as string (case-insensitive)

### Output:

- Returns the 2-letter **uppercase abbreviation**

### Example:

```python
get_state_abbreviation("New York")  → "NY"
```

## Behavior:

- Strips and capitalizes input as needed

- If the state is unknown, may return `None` or raise an error

---

## Used In:

- `nevi.py` or similar utilities

- `process_is_on_nevi_road()` from `roi.py`

- Location-to-code conversions for government/transport APIs