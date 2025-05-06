# Prediction Service

This service predicts **how many EVs will be registered** in a geographic area (ZCTA), used as a demand proxy for charging.

 The service defines only one function `predict_ev_registrations(zcta)` and expects ZCTA code as an input parameter.
 
## Main Function: `predict_ev_registrations(zcta)`
### What it does?

1. Takes a **ZCTA code** (ZIP-level area)
2. Uses the zcta code to look up:
- Total population
- State-level EV adoption curves
- Market trends
3. Returns an **integer value**: the estimated EV registrations in that area.
  

### Error Handling:  
- Returns exceptions like `TypeError`, `ValueError` if ZIP is invalid
- Other internal errors are caught and wrapped in an `ApiException` (via the router)
  
## Used in:
-  `roi.py` to simulate demand and traffic
-  `competition.py` may also use this to compare demand zones