# Open EI

This document explains the utility logic inside:  **`api/openei.py`**

This file is responsible for **fetching utility rate plans** from the [OpenEI API](https://openei.org) and updating system status.

---

## Purpose

We use OpenEI to retrieve **utility rate plan metadata**, including:

- Demand rates

- Energy charges

- Time-of-use schedules

- Capacity limits

---

## Function: `make_openei_request(latitude, longitude, sector, page=None)`

### Inputs:

- `latitude`, `longitude`: Location of the charging site

- `sector`: e.g., `residential`, `commercial`, etc.

- `page`: Optional plan ID to fetch a **specific utility rate plan**

### What It Does:

1. Builds a **GET** request to OpenEI:

```text
https://api.openei.org/utility_rates
```

1. Sends it with your credentials and filters:
    
    - `lat`, `lon`, `sector`, `radius=20`, `version=8`, etc.

2. Parses the JSON response and returns the full plan detail.

### Output:

- JSON plan object (if success)

- `None` if the request fails

### Error Handling:

- Logs error messages using `logging.error`

- Catches timeout or connection failures

---

## Function: `make_openei_page_request(page=None)`

### Purpose:

Used to fetch a **specific utility rate plan** directly by its `page` ID.

### Inputs:

- `page` (string): OpenEI rate plan ID

### Behavior:

- Same as `make_openei_request`, but without location (`lat/lon`) or sector

### Output:

- Returns JSON plan object or `None` on failure

---

## Function: `update_open_ei_status(status=True)`

### Purpose:

Notifies an internal service that OpenEI is **working** or **failing**, for monitoring.

### Inputs:

- `status`: Boolean flag (`True` or `False`)

### What It Does:

1. Sends a `PUT` request to:

```text
https://konect-api-<ENV>.azurewebsites.net/api/v1/openei/status
```

2. Includes JSON body like:

```json
{"isActive": true }
```

3. Environment is auto-detected using:

```python
os.getenv("ENV_TAG", "DEV")
```

### Output:

- JSON confirmation on success

- `None` if the call fails

---

## Used In

- `plan_parser.py` → via `make_openei_page_request()`

- `router/demand.py` → directly

- System-level health check pipelines