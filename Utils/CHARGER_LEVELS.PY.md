# Charger Levels Util

This document explains the logic inside the utility file:  
 **`utils/charger_levels.py`**

It is used across the competition analysis workflow to standardize, categorize, and compare **EV charger levels**.

---

##  Purpose

EV charging stations often support different **charging levels** (power outputs):

- Level 1: Low speed

- Level 2: Medium speed

- Level 3: Fast charging    

To simplify sorting and comparison, we **map these names to numeric indexes** (e.g. 1, 2, 3).  
We also handle stations with **multiple levels** cleanly.

---

##  Enum: `ChargerLevelIndex`

Used to convert level names into **consistent numeric values** for:

- Easier sorting

- Visual scaling
  
- Comparisons

```python
class ChargerLevelIndex(Enum):
    LEVEL_1  = 1
    LEVEL_2  = 2
    LEVEL_3  = 3
    MULTIPLE = 4
```

- `MULTIPLE = 4` is a special case for chargers that support **more than one level**.

##  Function: `level_name_to_index(name)`

Converts a **charger level string** to a numeric index based on the enum.

### Example:

```python
level_name_to_index("Level 3:  High (Over 40kW)")  # Returns 3
```

If the name is unrecognized or if multiple levels are detected later, it defaults to `MULTIPLE = 4`.

## Function: `levels_to_index(levels: list)`

Used when a **charger supports multiple levels**.
### Behavior:

- If there's **only one level**:  
    → Calls `level_name_to_index(level)` to get its index.

- If there are **multiple levels**:  
    → Returns `4` → the special enum value `MULTIPLE`. 

### Example:

```python
levels_to_index(["Level 2 : Medium (Over 2kW)"])  # → 2
levels_to_index(["Level 2", "Level 3"])           # → 4 (MULTIPLE)
```

##  Used In

- [`parse_charger()` in `competition.py`](competition_service.md#parse_chargerchargers)

- Nearest charger formatting

- Level count summaries