from utils import state_to_abbrev

# Test valid state names return correct abbreviations
def test_get_abbrev_valid_states():
    assert state_to_abbrev.state_name_to_abbreviation("California") == "CA"
    assert state_to_abbrev.state_name_to_abbreviation("Texas") == "TX"
    assert state_to_abbrev.state_name_to_abbreviation("New York") == "NY"


# Test invalid state names return None
def test_get_abbrev_invalid_states():
    assert state_to_abbrev.state_name_to_abbreviation("UnknownState") is None
    assert state_to_abbrev.state_name_to_abbreviation("") is None
    assert state_to_abbrev.state_name_to_abbreviation(None) is None


# ---------------- Value-Based Tests ----------------

# Test full list has expected abbreviations (partial sampling)
def test_get_abbrev_full_list_sample():
    expected_mappings = {
        "Florida": "FL",
        "Illinois": "IL",
        "Washington": "WA",
        "Arizona": "AZ"
    }
    for state, abbrev in expected_mappings.items():
        assert state_to_abbrev.state_name_to_abbreviation(state) == abbrev