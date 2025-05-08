# ROI Service

## Purpose

This service is the **core ROI calculation engine**. It performs full financial modeling for EV charger deployment over a 10-year timeline using utility rate plans, traffic, hardware, and other inputs.

---

## Main Class: `RoiService`

###  `calculateRoiAndNpv(...)`

Performs full financial analysis for a location and configuration.

#### Inputs:

- `plan_id`: OpenEI rate plan ID

- `predicted_ev_registrations`: Forecasted EV registrations (demand proxy)

- `driver_price_multiplier`: User pricing adjustment

- `hardware_config`: Charger cabinet configuration

- `hardware_cost`, `installation_cost`, `operating_cost`: CapEx and OpEx

- `federal_incentives`, `thirty_c_incentives`: Incentive amounts

- `peak_demand_per_car`: Peak demand assumption

- `utilization_assumption_percent`: Charger utilization (%)

- `discount_rate`: NPV discount rate (usually 3%)

- `node_lift`: Additional traffic influence

#### Workflow:

1. Calls `make_openei_page_request()` to fetch utility rate plan.

2. Initializes:
    
    - `DemandParser` for extracting pricing/time tier info
    
    - `EnergyConsumptionService` for simulating load
    
    - `RevenueCalculationService` for revenue + cash flow modeling
    
3. Runs a 10-year cash flow simulation and returns:
    
    - `npv`, ROI years/months
    
    - Costs (fixed, energy, demand)
    
    - Revenue, profit
    
    - Suggested number of ports
    
    - Cash flow per year
    

#### Returns:

- A dictionary with ROI detail + cash flow model

- If the utility plan is invalid, returns placeholders with `npv: -1`

---

###  `roi_and_nvp_calculations_sheet(...)`

Similar to `calculateRoiAndNpv()` but **outputs data for Excel generation** (used in `/roi_tables` endpoint).

#### Notes:

- Returns a formatted response that can be inserted into an Excel template

- Uses the same DemandParser and revenue modeling pipeline

---

## Used In:

- `roi.py` → for `/roi` and `/roi_tables` routes

- ROI + breakeven analysis logic