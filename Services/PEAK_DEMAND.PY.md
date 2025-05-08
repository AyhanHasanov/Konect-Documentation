# Peak Demand Service
## Purpose

This service estimates the **true electrical peak demand (in kW)** for a charging site, based on its hardware layout and number of incoming vehicles.  
It simulates how vehicles are plugged into available ports across **ports → chargers → cabinets → site**, and calculates the total power draw under physical and electrical constraints.

This is essential for estimating **hourly and monthly demand charges** in ROI and utility cost simulations.

## Function: calculate(hardware_configuration, predicted, peak_demand_per_car, utility_peak_demand_cap_kw, peak_demand_cap_kw=600)

### What it does:

1. Builds a **virtual model of the site hardware**:
   - Cabinets -> each with Chargers -> each with Ports.

2. Tries to **plug in** up to `predicted_cars` simultaneously, assigning each a power demand of `peak_demand_per_car` kW.
   
3. Prioritizes chargers and cabinets with the **most remaining capacity** to simulate real-world load balancing.

4. Calculates the **actual peak demand** at the site level by summing active loads, **capped** by:
    
    - The **cabinet/site power limits**
    
    - The **utility or artificial demand cap**


### Example Input:

```python
PeakDemandCalculationService.calculate(
    hardware_configuration = {
        "cabinets": [
            {
                "capacity": 200,
                "chargers": [
                    {"capacity": 100, "ports": 2},
                    {"capacity": 100, "ports": 2}
                ]
            }
        ]
    },
    predicted_cars = 3,
    peak_demand_per_car = 50,
    utility_peak_demand_cap_kw = 200,
    peak_demand_cap_kw = 180
)
```

### Example Output:

```python
150  # Total peak load handled (kW), respecting hardware and caps
```

### Error Handling

- Raises `Exception` if no free ports are available during simulation.

- Assumes clean and validated hardware config structure (caller responsibility).

---
## Used In:

- `DemandCalculationService.get_demand_table()`  
    → to simulate **hourly peak demand loads** for each hour/month

- `roi.py` (indirectly)  
    → affects demand cost modeling in ROI projections