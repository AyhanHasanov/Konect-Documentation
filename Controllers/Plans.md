# Plans Controller

-	The controller defines a Flask Route that accepts POST requests.

```python
@ROUTE.route('/api/v1/plans', methods=["POST"])
```
-	The controller iterates through each sector in OPENEI_SECTORS (Commercial, residential, industrial)

-	The controller calls get_plans(…)  (Plans service) with expected latitude, longitude, and utility.

-	The controller returns retrieved plans for each sector available in OPENEI SECTORS.
