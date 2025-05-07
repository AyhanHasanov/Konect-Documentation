# Geocoder
## Overview
The OpenCage Geocoding API file defines only one function `get_geocode`. It performs the same core function as Micrososft's Azure Geocode — converting a full address into latitude and longitude coordinates. The only difference is that the latter is done via a different provider.

## `get_geocode` function:
Expects the following input parameters:
- `address`
- `city`
- `state`
- `zip_code`

Creates a `full_address` string as follows: `{address}, {city}, {state}, {zip_code}` and using OpenCage's API converts it to coordinates.

Returns 2 values - longitude and latitude if the status response code is 200. Else the function returns a value error - " No response from OpenCage API".

### Example: 
**Input:**
```json
{
    "address": "1600 Amphitheatre Parkway",
    "city": "Mountain View",
    "state": "California",
    "zip": 94043
}
```
**Output:**
```json
{
	"latitude": 37.422, 
	"longitude": -122.084
}
```