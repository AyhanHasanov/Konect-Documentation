# Predict Controller
-	The controller defines a Flask Route that accepts POST requests.

```python
@ROUTE.route('/api/v1/plans', methods=["POST"])
```

-	The controller uses Prediction service and zcta_crosswalk service.

-	The controller extracts ZCTA (ZIP code tabulation area) or ZIP code (if ZCTA is not available) and then using the zcta_crosswalk service maps it to a ZCTA code.

-	The controller returns 400 if neither is provided or found.

-	The controller calls the predict_ev_registrations service function with the resolved ZCTA.

-	The controller handles and logs exceptions, returning a 500 error if prediction fails.

