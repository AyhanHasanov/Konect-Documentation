from api.geocoder_api import get_geocode
from api.azure_geocode import get_geocode as get_geocode_azure

address = "101 E Alma Ave"
city = "Boston"
state = "Massachusetts"
zip = " 02118"


expected = {
    "latitude": 42.332009,
    "longitude": -71.0737125
}


def test_geocoder_api():
    result = get_geocode(address, city, state, zip)
    assert result == expected

def test_azure_geocoder_api():
    coordinates = get_geocode_azure(address, city, state, zip)
    allowed_diff = 0.0015

    result = {
        "latitude" : abs(coordinates["latitude"]-expected["latitude"]),
        "longitude": abs(coordinates["longitude"]-expected["longitude"])
    }

    assert result["latitude"]  <= allowed_diff
    assert result["longitude"] <= allowed_diff