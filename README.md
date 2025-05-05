# Konect-Documentation

# 1. Overview
## 1.1. APIs
|API name|Brief description|
|:--|:--|
|Azure Geocode|Microsoft Azure's Geocode plays a crucial role by transforming user-submitted or database-stored addresses into coordinate points on a map. These coordinates are the foundational data points that allow the app to perform spatial analysis, display locations on interactive maps, and support routing or proximity searches.|
|Geocoder Api|Within the app, the geocoder functions as a key enabler for transforming user inputs or database records into mappable points. It bridges the gap between human-readable location data and the numerical coordinates needed for geographic computations and visualizations.|
|NEVI|NEVI stands for National Electric Vehicle Infrastructure, a federal initiative and set of standards aimed at expanding the electric vehicle (EV) charging network across the United States. Within the app, NEVI represents a critical framework for guiding infrastructure deployment, ensuring interoperability,and maintaining compliance with national EV charging policies.|
|Openchargermap|OpenChargeMap is an open-source database that catalogues electric vehicle (EV) charging stations worldwide. It serves as a centralized repository of detailed information on charging locations, including station types, connectors, availability, and geographic coordinates. This rich dataset is freely accessible and regularly updated, making it an invaluable resource for developers and users alike.|
|Openei|OpenEI (Open Energy Information) is an open-access platform offering a wealth of energy-related data, tools, and resources. It is developed and maintained by the U.S. Department of Energy to promote transparency, collaboration, and innovation in the energy sector.|

## 1.2. Controllers
|Endpoint|Method|Controller|
|:--|:--:|:--|
|/api/v1/competition|POST|[Competition](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Competition.md)
|/api/v1/demand_parser|POST|Demand
|/api/v1/demand_average|POST|Demand
|/api/v1/demand_time_parser|POST|Demand
|/api/v1/geocode|POST|Geocode
|/api/v1/health/flask|POST|Health
|/api/v1/health/spring|POST|Health
|/api/v1/health/openei|POST|Health
|/api/v1/nevi|POST|Nevi
|/api/v1/plans|POST|Plans
|/api/v1/predict|POST|Predict
|/api/v1/roi|POST|Roi
|/api/v1/roi_tables|POST|Roi
|/api/v1/score|POST|Score
|/api/v1/utilities|POST|Utility
|/api/v1/zip-zcta-crosswalk|POST|Zip-zcta-crosswalk

## 1.3. Services
-	Area
-	Competition
-	Demand_calculation
-	Energy_consumption_calculation
-	Finance_util
-	Nevi
-	Peak_demand
-	Plan_parser
-	Plans
-	Prediction
-	Revenue_calculation
-	ROI_service
-	Score
-	Utilities
-	ZCTA_crosswalks
