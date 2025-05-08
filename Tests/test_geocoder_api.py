from api.geocoder_api import get_geocode
from api.azure_geocode import get_geocode as get_geocode_azure

address = "17 Melnea Cass Blvd"
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
    #Fails because azure's api calculates the coordinates a little bit differently from the openchargermaps geocoder
    #Problem: how to convert and check coordinates beforehand ???
    result = get_geocode_azure(address, city, state, zip)
    assert result == expected
