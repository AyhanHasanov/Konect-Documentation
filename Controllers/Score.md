# Score controller
- The controller uses the following services:
	- Area
	- Competition
	- Score

- The controller uses `process_utility_cost`, `process_ev_registration`, `process_zcta` functions from the ROI controller.
- The controller defines one route that accepts only POST requests and 4 functions:

```python
@ROUTE.route('/api/v1/score', methods=["POST"])
```

## Key Factors:

- **Market Potential** – Uses local population and income data to assess demand.
- **Competition** – Analyzes nearby chargers and distances to gauge saturation.
- **Financial Viability** – Models energy costs, pricing, utilization, and revenue.
- **NEVI Eligibility** – Flags sites on federally funded EV corridors.
- **EV Adoption** – Considers predicted local EV registrations.

## For Each Site:
- Gathers demographic and financial data.
- Calculates competition from nearby chargers.
- Combines all data to generate a set of subscores and a final score.

Returns a list of scored sites, with each score broken into categories (e.g. market, financial, infrastructure), so stakeholders can compare and prioritize locations for EV charger deployment.