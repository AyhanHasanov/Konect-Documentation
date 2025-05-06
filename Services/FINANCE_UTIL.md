# Finance_util Service
>**NOTE: The hourly_distribution is currently hardcoded while it is meant to come from Driivz**

This service provides a **prediction of hourly EV charging station visits** based on historical usage data and a known weekly total. It **distributes total visits over 24 hours** using a predefined hourly proportion profile.

## Purpose

The goal of the service is to help **forecast how visits are distributed across the day**, which supports:

-   Energy consumption modeling
-   Revenue forecasting per hour
-   Charging infrastructure planning
-   Load balancing or peak-hour readiness
    

It’s particularly useful when you **know the total number of expected visits per week** and want to **understand the visit breakdown per hour** across a typical day.


## Main Function: `predict_visits_by_hour(weekly_visits)`

This is the primary entry point of the service.

### Inputs:
-   `weekly_visits`: An integer or float representing the **total number of expected visits per week**.
    
### Workflow:
1.  Calls `get_hourly_proportions()` to retrieve a **normalized hourly distribution** of charging visits.
2.  Multiplies each hourly proportion by the `weekly_visits` count to get **visit predictions for each hour of the day**.
    
### Output:

Returns a **list of 24 values**, where each entry is the **predicted number of visits for that hour** in a day.


### Helper Function: `get_hourly_proportions()`

Returns a **normalized 24-hour distribution** (as a Pandas Series) based on hardcoded visit counts.


### Why Is This Service Needed?

It plays a key role in **simulating or predicting demand patterns** at EV charging stations, especially when:

-   You only know aggregate visit volumes but want a **finer-grained hourly breakdown**.
    
-   Planning or optimization requires insight into **daily charging activity curves**.
    
-   Feeding models like **energy usage, queueing systems, pricing**, or **charger availability forecasts**.
    