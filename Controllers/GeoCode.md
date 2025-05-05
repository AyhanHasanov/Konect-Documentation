# Geocode Controller

The Geocode controller attributes for converting descriptive location Information - such as street addresses, place names, or postal codes - into geographic coordinates (latitude and longitude). This process, known as geocoding, is fundamental for applications that operate with spatial data or require precise mapping capabilities. In order to achieve its purpose the controller uses Microsoft’s Azure API that actually makes the desired conversion.

- Defines a Flask route that accepts POST requests:
```python
@ROUTE.route('/api/v1/geocode', methods=["POST"])
```

- Expects a JSON payload with address, city, state, and zip.

- Calls *get_geocode* from the azure_geocode module to get geographic coordinates.

- Handles two error cases:
o	**ValueError**: Due to bad input; returns a 400 response with a structured error.
o	**General Exception**: For unexpected internal failures; returns a 500 error with a detailed log.
