
This document explains the **ROI router logic (`roi.py`)** used to estimate the return on investment for installing EV chargers based on utility plans, traffic, and demographic data.

---

# Endpoints and Workflow

## /api/v1/roi/

```python
@ROUTE.route('/api/v1/roi', methods=["POST"])
```

### How it works:

Receives a POST payload like:

```json
{
  "latitude": 34.05,
  "longitude": -118.25,
  "state": "CA",
  "zip": "90001",
  "planId": "utility_rate_id",
  "planName": "...",
  "planSector": "...",
  "hardwareCost": 100000,
  "installCost": 20000,
  "operatingCost": 3000,
  "driverPriceMultiplier": 2.5,
  "utilization": 18,
  "hardwareConfig": [...],
  "kwhPerVisit": 25,
  "has30c": true,
  "withNodes": true
}
```

### Steps:

1. **ZCTA & Population Prediction**
    
    - Calls `zip_to_zcta(zip)` → to get the ZCTA.
    
    - Runs `predict_ev_registrations(zcta)` and `get_total_population(zcta)`.
    
2. **Node Lift**
    
    - Uses `run_nodes_lift_service(latitude, longitude)` to assess:
        
        - Node lift score
        
        - Regional traffic estimates
        
3. **ROI + Cash Flow Calculation**
    
    - Uses `RoiService.calculateRoiAndNpv(...)`
    
    - Returns detailed cash flows and average visits.
    
4. **Breakeven + Graphs**
    
    - Computes `breakevenYear`, `income_return_graph`, and `scatterGraph`.
    
5. **Extras:**
    
    - Checks NEVI route status → `get_nevi_route(...)`
    
    - Calculates estimated **weekly and monthly kWh consumption**
    
    - Returns `suggestedNumberOfPorts`
    
    - Prepares final structured JSON response

### Output (partial):

```json
{
  "npv": 52000,
  "roiInYears": 4,
  "roiInMonths": 48,
  "capitalExpense": 120000,
  "operatingExpense": 36000,
  "isInvestmentRefundable": true,
  "avgWeeklyVisits": 160,
  "weeklyEnergyConsumptionKwh": 4000,
  "scatterGraphPerHour": [ { "hour": 0, "kwh": 10, "averageCost": 0.13, ... } ],
  ...
}
```

## /api/v1/roi_tables

```python
@ROUTE.route('/api/v1/roi_tables', methods=["POST"])
```

### Purpose:

This endpoint generates Excel ROI summary used for further analysis.

### Input (example):

```json
{
  "utilityPlanId": "utility_id",
  "hardwareCost": 90000,
  "installCost": 15000,
  "operatingCost": 2500,
  "hardwareConfigCollection": [...],
  "utilization": 15,
  "incentives": 10000,
  "has30c": false,
  "driverPriceMultiplier": 2.0,
  "latitude": 34.05,
  "longitude": -118.25,
  "zip": "90001"
}
```

### Internals:

- ZCTA and EV predictions are calculated.

- NEVI traffic and node lift pulled.

- Passes all params to `RoiService.roi_and_nvp_calculations_sheet(...)`.

### Output:

- Returns a JSON structure representing **ROI data table**.

## Supporting Functions (called internally)

|Function|Purpose|
|---|---|
|`process_cash_flow()`|Main driver of ROI/cash flow logic via `RoiService`|
|`process_total_cost()`|Computes net CAPEX after incentives|
|`process_is_on_nevi_road()`|Determines if location is near a NEVI-designated route|
|`get_weekly_energy_consumption()`|Calculates weekly kWh demand|
|`process_scatter_graph()`|Builds 24-hour kWh + cost + pricing comparison graph|
|`process_income_and_return()`|Builds yearly graph of ROI vs. time|
|`process_accumulated_return()`|Tracks cumulative return per year|

---

## Used Services & Utilities

- `RoiService` – ROI, NPV, suggested ports

- `node_lifts_calculations` – regional traffic impact

- `plans`, `zcta_crosswalk`, `prediction`, `area`, `finance_util`

- `get_nevi_route()` – NEVI route proximity

- `ApiException` – Unified error handling