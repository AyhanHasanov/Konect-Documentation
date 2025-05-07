# Every_state_lat_long Utility

This file contains one function `get_list_of_locations_per_state()` that returns a hardcoded list of geographic coordinate (latitude and longitude), along with associated cities and U.S. state. Each entry in the list represents one location per state, presumably intended to serve as a representative or capital city (though not always accurately so). 

- Return Type: A list of dict objects
- Each dictionary contains:
	- latitude: float
	- longitude: float
	- city: str
	- state: str
```python
def get_list_of_locations_per_state():
	return [
	{
		"latitude": -68.962946,
		"longitude": -135.35275,
		"city": "Birmingham",
		"state": "Alabama"
	},
	...
	]
```