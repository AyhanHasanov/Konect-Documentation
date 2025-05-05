# NEVI Controller

NEVI represents a critical framework for guiding infrastructure deployment, ensuring interoperability, and maintaining compliance with national EV charging policies.

- Defines a Flask route that accepts only POST requests:

```python
@ROUTE.route('/api/v1/nevi', methods=["POST"])
```
-	The controller expects a JSON with latitude, longitude, state and optionally radiusMeters.

-	The controller  fetches NEVI routes for the given state and checks if the location is within the proximity using geospatial logic.

-	Determines if a given location lies within a specified radius of a NEVI route.

-	Returns either true or false.

-	If the input state is incorrect – the function of the endpoint returns a bad request 400 error.
