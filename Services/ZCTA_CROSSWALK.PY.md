### Purpose

Converts **ZIP codes** to **ZCTA** (ZIP Code Tabulation Area) — a standardized geographic unit used by the US Census Bureau.

This helps normalize ZIP inputs for data queries like population, EV prediction, etc.

---

## Main Function: `zip_to_zcta(zip_code: int)`

### What it does:

1. Receives a 5-digit ZIP code

2. Returns the **matching ZCTA code** using a lookup table or algorithm

### Why ZCTA matters:

- Many government and research datasets use ZCTA instead of ZIP

- Required for population queries (`area.py`) and predictions

### Error Handling:

- Raises exceptions if the ZIP is invalid or not found

- These are caught by routers like `roi.py` and shown as user-friendly error messages

---

### Used In:

- `roi.py` → during ZCTA normalization

- `prediction.py` → EV forecasting needs ZCTA

- `area.py` → Population lookups use ZCTA