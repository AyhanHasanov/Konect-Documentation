from utils import charger_levels


# Test correct mapping from charger level name to index
def test_level_name_to_index_valid():
    assert charger_levels.level_name_to_index("Level 1 : Low (Under 2kW)") == 1
    assert charger_levels.level_name_to_index("Level 2 : Medium (Over 2kW)") == 2
    assert charger_levels.level_name_to_index("Level 3:  High (Over 40kW)") == 3


# Test unknown charger level returns MULTIPLE index (4)
def test_level_name_to_index_invalid():
    assert charger_levels.level_name_to_index("Unknow Level") == 4
    assert charger_levels.level_name_to_index("") == 4
    assert charger_levels.level_name_to_index(None) == 4


# ---------------- Value-Based Tests ----------------

# Test levels_to_index returns MULTIPLE index when multiple levels provided
def test_levels_to_index_multiple_levels():
    levels = ["Level 1 : Low (Under 2kW)", "Level 2 : Medium (Over 2kW)"]
    assert charger_levels.levels_to_index(levels) == 4


# Test levels_to_index correctly maps a single known level
def test_levels_to_index_single_level():
    levels = ["Level 1 : Low (Under 2kW)"]
    assert charger_levels.levels_to_index(levels) == 1


# Test levels_to_index correctly handles unknown level name
def test_levels_to_index_unknown_level():
    levels = ["Unknown level"]
    assert charger_levels.levels_to_index(levels) == 4