from services.nevi import get_nevi_route

def test_get_nevi_route_true():
    # Basic scenario
    # Expected: True
    # Within a radius of 5000m there is a NEVI route

    lat   = 36.414893
    lon   = -77.635099
    state = "North Carolina"

    result = get_nevi_route(lat, lon, state)

    assert result == True

def test_get_nevi_route_false():
    # Basic scenario
    # Expected: False
    # Within a radius of 5000m there is NOT a NEVI route

    lat = 34.151871
    lon = -78.275451
    state = "North Carolina"

    result = get_nevi_route(lat, lon, state)

    assert result == False
