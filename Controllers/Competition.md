# Competition Controller

- Defines a Flask route that accepts POST requests:
```python
@ROUTE.route('/api/v1/competition', methods=["POST"])
```

- The controller extracts latitude and longitude from the request's JSON payload.
- The controller calls the *get_competition* service(**LINK TO THE SERVICE**) function with the extracted coordinates and returns its result.
