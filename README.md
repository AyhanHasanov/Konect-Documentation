# Konect-Documentation

# 1. Overview

## 1.0. Structure overview with links:
- **flask-service/**
  - **api/**
    - [azure_geocode](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/AZURE_GEOCODE.md)
    - [geocoder_api](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/GEOCODER_API.md)
    - [nevi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/NEVI.PY.md)
    - [openchargemap](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/OPENCHARGEMAP.PY.md)
    - [openei](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/OPENEI.PY.md)
  - **controllers/**
    - [competition](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Competition.md)
    - [demand](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Demand.md)
    - [geocode](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/GeoCode.md)
    - [health](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/HEALTH.PY.md)
    - [nevi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/NEVI.md)
    - [plans](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Plans.md)
    - [predict](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Predict.md)
    - [roi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/ROI.PY.md)
    - [score](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Score.md)
    - [utility](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/UTILITY.PY.md)
    - [zip_zcta_crosswalk](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/ZIP_ZCTA_Crosswalk.md)
  - **services/**
    - [area](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/AREA.PY.md)
    - [competition](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/COMPETITION.PY%20(SERVICE).md)
    - [demand_calculation](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/DEMAND_CALCULATION.PY.md)
    - [energy_consumption_calculation](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/ENERGY_CONSUMPTION_CALCULATION.md)
    - [finance_util](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/FINANCE_UTIL.md)
    - [nevi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/NEVI.md)
    - [peak_demand](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PEAK_DEMAND.PY.md)
    - [plan_parser](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PLAN_PARSER.PY.md)
    - [plans](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PLANS.PY.md)
    - [prediction](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PREDICTION.PY.md)
    - [revenue_calculation](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/REVENUE_CALCULATION.md)
    - [roi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/ROI_SERVICE.PY.md)
    - [score](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/SCORE.md)
    - [utilities](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/UTILITIES.PY%20(SERVICE).md)
    - [zip_zcta_crosswalk](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/ZCTA_CROSSWALK.PY.md)
  - **utils/**
    - [charger_levels](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/CHARGER_LEVELS.PY.md)
    - [data](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/DATA.PY.md)
    - [database](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/DATABASE.md)
    - [date](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/DATE.PY.md)
    - [every_state_lat_long](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/EVERY_STATE_LAT_LONG.md)
    - [fetch_overpass_data](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/FETCH_OVERPASS_DATA.PY.md)
    - [log](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/LOG.PY.md)
    - [node_lifts_calculations](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/NODE_LIFTS_CALCULATIONS.PY.md)
    - [response_error](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/RESPONSE_ERROR.PY.md)
    - [state_to_abbrev](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Utils/STATE_TO_ABBREV.PY.md)


## 1.1. APIs
|API name|Brief description|
|:--|:--|
|[Azure Geocode](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/AZURE_GEOCODE.md)|Microsoft Azure's Geocode plays a crucial role by transforming user-submitted or database-stored addresses into coordinate points on a map. These coordinates are the foundational data points that allow the app to perform spatial analysis, display locations on interactive maps, and support routing or proximity searches.|
|[Geocoder Api](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/GEOCODER_API.md)|Within the app, the geocoder functions as a key enabler for transforming user inputs or database records into mappable points. It bridges the gap between human-readable location data and the numerical coordinates needed for geographic computations and visualizations.|
|[NEVI](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/NEVI.PY.md)|NEVI stands for National Electric Vehicle Infrastructure, a federal initiative and set of standards aimed at expanding the electric vehicle (EV) charging network across the United States. Within the app, NEVI represents a critical framework for guiding infrastructure deployment, ensuring interoperability,and maintaining compliance with national EV charging policies.|
|[Openchargermap](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/OPENCHARGEMAP.PY.md)|OpenChargeMap is an open-source database that catalogues electric vehicle (EV) charging stations worldwide. It serves as a centralized repository of detailed information on charging locations, including station types, connectors, availability, and geographic coordinates. This rich dataset is freely accessible and regularly updated, making it an invaluable resource for developers and users alike.|
|[Openei](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/APIs/OPENEI.PY.md)|OpenEI (Open Energy Information) is an open-access platform offering a wealth of energy-related data, tools, and resources. It is developed and maintained by the U.S. Department of Energy to promote transparency, collaboration, and innovation in the energy sector.|

## 1.2. Controllers
|Endpoint|Method|Controller|
|:--|:--:|:--|
|/api/v1/competition|POST|[Competition](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Competition.md)
|/api/v1/demand_parser|POST|[Demand](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Demand.md)
|/api/v1/demand_average|POST|[Demand](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Demand.md)
|/api/v1/demand_time_parser|POST|[Demand](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Demand.md)
|/api/v1/geocode|POST|[Geocode](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/GeoCode.md)
|/api/v1/health/flask|POST|[Health](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/HEALTH.PY.md)
|/api/v1/health/spring|POST|[Health](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/HEALTH.PY.md)
|/api/v1/health/openei|POST|[Health](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/HEALTH.PY.md)
|/api/v1/nevi|POST|[Nevi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/NEVI.md)
|/api/v1/plans|POST|[Plans](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Plans.md)
|/api/v1/predict|POST|[Predict](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Predict.md)
|/api/v1/roi|POST|[Roi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/ROI.PY.md)
|/api/v1/roi_tables|POST|[Roi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/ROI.PY.md)
|/api/v1/score|POST|[Score](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/Score.md)
|/api/v1/utilities|POST|[Utility](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/UTILITY.PY.md)
|/api/v1/zip-zcta-crosswalk|POST|[Zip-zcta-crosswalk](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Controllers/ZIP_ZCTA_Crosswalk.md)

## 1.3. Services
-	[Area](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/AREA.PY.md)
-	[Competition](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/COMPETITION.PY%20(SERVICE).md)
-	[Demand_calculation](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/DEMAND_CALCULATION.PY.md)
-	[Energy_consumption_calculation](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/ENERGY_CONSUMPTION_CALCULATION.md)
-	[Finance_util](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/FINANCE_UTIL.md)
-	[Nevi](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/NEVI.md)
-	[Peak_demand](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PEAK_DEMAND.PY.md)
-	[Plan_parser](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PLAN_PARSER.PY.md)
-	[Plans](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PLANS.PY.md)
-	[Prediction](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/PREDICTION.PY.md)
-	[Revenue_calculation](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/REVENUE_CALCULATION.md)
-	[ROI_service](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/ROI_SERVICE.PY.md)
-	[Score](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/SCORE.md)
-	[Utilities](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/UTILITIES.PY%20(SERVICE).md)
-	[ZCTA_crosswalks](https://github.com/AyhanHasanov/Konect-Documentation/blob/main/Services/ZCTA_CROSSWALK.PY.md)
