import pytest
from unittest.mock import patch
from services import utilities

# Mock plan data for testing
mock_plans = [
    {"utility": "Utility A"},
    {"utility": "Utility B"},
    {"utility": "Utility A"},  # Duplicate utility to test uniqueness
    {"name": "No Utility Field"}
]

# Test get_unique_utility_providers returns unique utility names
def test_get_unique_utility_providers_returns_unique():
    result = utilities.get_unique_utility_providers(mock_plans)
    assert sorted(result) == ["Utility A", "Utility B"], "Should return unique utility names sorted."

# Test get_unique_utility_providers returns empty list if no utilities found
def test_get_unique_utility_providers_empty_when_no_utility():
    result = utilities.get_unique_utility_providers([{"name": "No Utility Field"}])
    assert result == [], "Should return empty list if no utility key is present."

# Test get_utilities returns the correct unique utility list when API returns valid data
@patch("services.utilities.make_openei_request")
def test_get_utilities_returns_correct_data(mock_request):
    mock_request.return_value = {"items": mock_plans}
    result = utilities.get_utilities(0, 0, "residential")
    assert sorted(result) == ["Utility A", "Utility B"], "Should return correct unique utility names."

# Test get_utilities returns empty list when API returns no items
@patch("services.utilities.make_openei_request")
def test_get_utilities_returns_empty_when_no_items(mock_request):
    mock_request.return_value = {"items": []}
    result = utilities.get_utilities(0, 0, "residential")
    assert result == [], "Should return empty list when no plans are returned."

# Test get_utilities returns empty list when API call returns None
@patch("services.utilities.make_openei_request")
def test_get_utilities_returns_empty_when_no_data(mock_request):
    mock_request.return_value = None
    result = utilities.get_utilities(0, 0, "residential")
    assert result == [], "Should return empty list when API returns None."

# ---------------- Value-Based Tests ----------------

# Test that get_unique_utility_providers handles completely empty input correctly
def test_get_unique_utility_providers_empty_input():
    result = utilities.get_unique_utility_providers([])
    assert result == [], "Should return empty list when given empty input."

