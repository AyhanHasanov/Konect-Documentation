# Health Controller

This document explains the **health.py route logic** step-by-step.  
The whole workflow is to **monitor system availability** by verifying that the Flask server, the external Spring Boot API, and the OpenEI utility rate API are all functioning correctly across various U.S. states and sectors.

---

## Endpoints and Workflow

---

### `/api/v1/health/flask`

```python
@ROUTE.route('/api/v1/health/flask', methods=["POST"])
```

#### How it works:

- Returns a simple confirmation that the **Flask server is running**:

```json
{
  "status": "Flask is up and running"
}
```

- Always responds with **HTTP 200** if the server is operational.

### `/api/v1/health/spring`

```python
@ROUTE.route('/api/v1/health/spring', methods=["POST"])
```
#### How it works:

- Reads the current environment tag from the `ENV_TAG` environment variable (defaults to `"DEV"`).

- Sends a **GET request** to the Spring Boot actuator health endpoint:

```http
https://konect-api-{env_tag}.azurewebsites.net/api/v1/actuator/health
```

- If the response is successful (`200 OK`), returns:

```json
{
  "status": "Spring is up and running for dev"
}
```

- If Spring is down or unreachable, it returns a custom error message and status.

### `/api/v1/health/openei`

```python
@ROUTE.route('/api/v1/health/openei', methods=["POST"])
```

#### How it works:

- **Loops through a list of representative U.S. locations** by calling:

```python
get_list_of_locations_per_state()
```

- For each location, sends **OpenEI API requests** for three sectors:
    
    - Commercial
    
    - Residential
    
    - Industrial

- Uses the helper function `send_request_for_state(state, city, latitude, longitude)` to:
    
    - Send requests with OpenEI API key and location-based parameters
    
    - Catch HTTP and JSON decoding errors
    
    - Record status and any issues in a results dictionary

- Aggregates errors and response summaries by state and sector.

- Updates the **OpenEI system status** using:

```python
update_open_ei_status(True/False)
```

Based on whether errors occurred.

#### Returns:

- A summary of which states passed/failed

- A detailed `errors` list with error messages per state + sector

- An overall count of failures


#### Example Output:

```json
{
  "errors_count": 2,
  "errors": [
    {
      "state": "AZ",
      "city": "Phoenix",
      "sector": "Commercial",
      "error": "Request timeout"
    },
    ...
  ],
  "states_covered": ["CA", "TX", "NY", ...],
  "checks": {
    "CA": {
      "latitude": 34.05,
      "longitude": -118.24,
      "sectors": {
        "Commercial": { "status_code": 200, "has_body": true },
        "Residential": { ... }
      }
    }
  }
}
```

If any unexpected error occurs during processing, a `500 Internal Server Error` is returned with details.