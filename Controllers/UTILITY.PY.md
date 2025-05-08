# Utility Controller

This document explains the **utility.py route logic** step-by-step.  
The route collects a list of **electric utility providers** available at a given location, along with the **sectors** (e.g. Commercial, Residential) they serve.

---

## Endpoint and Workflow

### `/api/v1/utilities`

```python
@ROUTE.route('/api/v1/utilities', methods=["POST"])
```

### How it works:

- Receives a POST request:

```json
{
  "latitude": 42.123,
  "longitude": -71.456
}
```

- Iterates over the list of OpenEI sectors:

```python
OPENEI_SECTORS = ["Commercial", "Residential", "Industrial"]
```

- For each sector:
    
    - Calls `get_utilities()` with the coordinates and sector
    
    - Collects all unique utilities and maps them to their applicable sectors
    
- Builds and returns:

```json
[
  {
    "name": "Utility Provider A",
    "sectors": ["Commercial", "Residential"]
  },
  ...
]
```

- If **no utilities found**, returns a fallback default:

```json
[
  {
    "name": "General",
    "sectors": ["Commercial"]
  }
]
```

---

## Used Services:

- `get_utilities()` in `services/utilities.py`

- `make_openei_request()` from `api/openei.py`