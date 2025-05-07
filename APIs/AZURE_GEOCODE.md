# Azure Geocode
## Overview
The Azure Geocode file defines only one function `get_geocode` which uses Microsoft's Azure API to convert human readable addresses into geographical coordinates (latitude and longitude)

## `get_geocode` function:
Expects the following input parameters:
- `address`
- `city`
- `state`
- `zip_code`

Creates a `full_address` string as follows: `{address}, {city}, {state}, {zip_code}` and using Azure's API converts it to coordinates.

Returns 2 values - longitude and latitude if the status response code is 200. Else the function returns a value error - " No response from Azure Maps API ".

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