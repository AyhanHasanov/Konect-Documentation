# DEMAND CONTROLLER
-	Uses Plan_parser service and Demand_calculation service.

-	The controller defines 3 routes all of which accept only POST requests.
```python
@ROUTE.route('/api/v1/demand_parser', methods=["POST"])
def get_demand_parser():
...
@ROUTE.route('/api/v1/demand_average', methods=["POST"])
def get_demand_average():
...
@ROUTE.route('/api/v1/demand_time_parser', methods=["POST"])
def get_demand_time_parser():
```
-	All 3 functions (get_demand_parser(), get_demand_average(), get_demand_time_parser()) use the OPEN API.

-	get_demand_parser() is used to extract and return the demand charge tiers from a utility rate plan stored in the OPENEI database, using a specific page ID sent in the request.

-	get_demand_average() – не ми е ясно какво точно прави???

-	get_demand_time_parser() returns detailed information about when demand charges apply throughout the day, based on a specific utility rate plan. It breaks this down by month, weekday/weekend, and tier, showing the exact hours demand charges are active and how frequently they occur. This helps users understand the time-based structure of their electricity pricing.
