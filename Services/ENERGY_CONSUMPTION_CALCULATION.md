# Energy Consumption Calculation Service
## Overview
The service defines a single class with 3 static functions and 1 function outside the scope of the class

This `EnergyConsumptionService` is designed to model and estimate **energy consumption and cost** for an EV charging station based on:

-   Hourly car visit forecasts
-   Charger hardware configuration
-   Utilization assumptions
-   Tiered energy pricing
   
## 1. `get_energy_consumption_table(...)`
### Input parameters:
-  `expected_car_visits_per_hour`: forecasted number of EVs arriving each hour (grouped by month and weekday/weekend).
- `hardware_config`: structure of EV chargers (cabinets, chargers,  ports).
-  `utilization_assumption_percent`: how much of the max capacity you realistically expect to use.
    
Calculates:

-   Estimated energy use per hour    
-   Max cars that can be handled per hour
-   Estimated handled visitors per week
    
Logic:

-   Each charging port can serve 3 cars/hour    
-   Each car consumes 25 kWh
-   Caps car visits to hardware capacity (`actual_cars = min(car_count, max_supported)`)
    

### Outputs:

-   `energy_consumption_table` → kWh used per hour
-   `max_serviced_cars_table` → max actual cars handled per hour
-   `handled_weekly_visitors` → estimated cars per **average week** (5 weekdays + 2 weekend days)
    
    
## 2. `calculate_energy_consumption(energy_consumption_map)`
The function totals up all kWh across months, days, and hours.

``` python
total = sum of all hour values in energy_consumption_map
```



## 3. `calculate_energy_consumption_cost(...)`
### Input parameters:
- `energy_consumption_per_hour`: the consumption of energy for every hour grouped by months, weekdays and weekends.
- `tiers_energy_cost`: price per kWh for different pricing tiers.
- `time_ranges`: defines which hours in a day fall under which pricing tier.
    
Estimates **monthly electricity cost** by:
-   Multiplying energy per hour × tier price based on hour
-   Summing over all hours
-   Scaling by **30 days** (assuming a 30-day month)
    

```python
cost = hourly_kwh × tier_rate × 30
```

### Helper function `get_energy_cost_per_hour_map(...)`
A helper function `get_energy_cost_per_hour_map(...)` to map hours to tiers.

The function generates a table of **energy costs per hour**, based on:

-   Tiered energy rates (`tiers_energy_cost`)
-   Time range mappings (e.g. tier 1 = 8am–6pm)
    

#### Example:

If tier 1 costs $0.20/kWh and the hour 14 (2 PM) is in tier 1, and 100 kWh is used:

```
cost = 100 × 0.20 = $20.00 
```