# Revenue Calculation Service

## Overview

The `RevenueCalculationService` is responsible for estimating the **monthly revenue generated** by an EV charging station based on energy usage patterns, tiered energy pricing, and driver-specific pricing multipliers. It performs a **time-of-use billing simulation** based on historical consumption and pricing rules.

The service itself is defined as a class and defines one function - `calculate(energy_consumption_table, tiers_energy_cost, time_ranges, driver_price_multiplier)`.

## Purpose

This service helps answer:  
**“How much revenue will a charging station earn in a month, based on when drivers charge and how much energy they consume?”**

It’s primarily used to:
-   Estimate profitability of EV chargers
-   Support pricing strategy decisions
-   Evaluate time-of-use (TOU) tariff impacts    
-   Simulate different pricing scenarios for driver groups (e.g., fleet vs. retail customers)
 

## Main Function: `calculate(...)`

This is a **static method** and it's the core function that performs the revenue calculation.

### Inputs:

-   `energy_consumption_table`:  
    Dictionary organized by month, day type (weekdays/weekends), and hour — shows how much energy (in kWh) is consumed at each hour.
    
-   `tiers_energy_cost`:  
    Dict mapping pricing tiers (e.g., "off-peak", "peak") to base cost per kWh.
    
-   `time_ranges`:  
    Defines which hours fall into which pricing tier, for each month and day type. Example: 16:00–21:00 might be "peak" in June weekdays.
    
-   `driver_price_multiplier`:  
    A scalar multiplier applied to base energy cost — simulates different billing rules (e.g., profit markup or discounted fleet rates).
    
### Workflow:

1.  **Applies price multiplier** to each pricing tier to get **final driver-facing price**.
2.  Loops over each month, then day type (weekday/weekend), then hour.
3.  Determines which tier applies to each hour.
4.  Calculates **revenue for that hour** as:

    `revenue = energy_consumed * driver-tier-rate` 
    
5.  Aggregates the per-hour revenue into a **per-month revenue table**.    
6.  Sums the table and multiplies by **30**, assuming each entry represents **a single day's data**, to extrapolate total monthly revenue.
    

### Output:
Returns a dictionary:
```python
{ "total": <monthly_revenue>, "table": <detailed_hourly_revenue_per_month> }
```