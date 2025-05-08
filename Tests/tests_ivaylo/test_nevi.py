from services.nevi import get_nevi_route

def test_location_on_nevi_route():
    # Example coordinates
    latitude = 34.0522
    longitude = -118.2437
    state = "California"

    result = get_nevi_route(latitude, longitude, state)
    print(f"NEVI Test (expected True): {result}")
    assert result == True

    # As expected Result = True

def test_location_off_nevi_route():
    # Example coordinates unlikely on NEVI route

    latitude = 48.8566
    longtitude = 2.3522
    state = "California"

    result = get_nevi_route(latitude, longtitude, state)
    print(f"NEVI Off-Route Test (expected False): {result}")
    assert result == False

    # As expected Result = False