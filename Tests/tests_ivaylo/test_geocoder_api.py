from api.geocoder_api import get_geocode
from api.azure_geocode import get_geocode as get_azure_geocode

from geopy.distance import geodesic

address = "1600 Pennsylvania Ave NW"
city = "Washington"
state = "District of Columbia"
zip_code = "20500"

# Expected coordinates
expected = {
    "latitude": 38.8976763,
    "longitude": -77.0365298
}

# Because from the different API's the result differs slightly from the expected coordinates
# We make this func in which we give 50m tolerance
def assert_tolerance(actual, expected, tolerance_meters = 50):
    actual_point = (actual["latitude"], actual["longitude"])
    expected_point = (expected["latitude"], expected["longitude"])

    distance = geodesic(actual_point, expected_point).meters

    assert distance < tolerance_meters, f"Dislike too large {distance} meters"


def test_geocode_api():
    result = get_geocode(address, city, state, zip)
    print(f"Geocoder API Test result: {result}")
    assert_tolerance(result, expected)
    # Test Fails because it calculates 113m away from the target, but I leave it like that because in the project
    # Azure Geocode is used


def test_azure_geocode_api():
    result = get_azure_geocode(address, city, state, zip)
    print(f"Azure Geocoder API Test result: {result}")
    assert_tolerance(result, expected)

    # Returns expected result with the tolerance of 50m