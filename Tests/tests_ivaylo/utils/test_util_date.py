import pytest

from utils import date

@pytest.mark.parametrize("index, expected", [
    (0, "jan"),
    (1, "feb"),
    (2, "mar"),
    (3, "apr"),
    (4, "may"),
    (5, "jun"),
    (6, "jul"),
    (7, "aug"),
    (8, "sep"),
    (9, "oct"),
    (10, "nov"),
    (11, "dec")
])
def test_get_month_abbrev_valid_indices(index, expected):
    result = date.get_month_abbreviation(index)

    assert result == expected, f"Expected {expected} for index {index}, got {result}"


@pytest.mark.parametrize("invalid_index", [-1, 12, 100, -5])
def test_get_month_abbrev_invalid_indices(invalid_index):
    with pytest.raises(ValueError) as exc_info:
        date.get_month_abbreviation(invalid_index)

    assert str(exc_info.value) == "Index must be in the range 0-11."


# ---------------- Value-Based Tests ----------------

# Test that get_month_abbreviation returns correct type
def test_get_month_abbrev_returns_string_type():
    result = date.get_month_abbreviation(0)

    assert isinstance(result, str), "Expected the result to be a string."