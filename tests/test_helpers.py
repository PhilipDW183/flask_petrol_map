from petrol_locations.helpers import geocode_postcode
from unittest.mock import MagicMock, patch
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
import pytest

class StubResponse:
    def __init__(self, longitude, latitude):
        self.longitude = longitude
        self.latitude = latitude

@pytest.fixture
def mocked_geolocator():
    mock = MagicMock()
    mock.geocode.return_value = StubResponse(0, 0)
    with patch("petrol_locations.helpers.Bing", return_value=mock):
        yield mock

def test_geocode_postcode_success(mocked_geolocator):
    postcode = 'SW1A 2AA'
    result = geocode_postcode(postcode)
    assert result == (0, 0)
    mocked_geolocator.geocode.assert_called_once_with(query={'postalCode': postcode, 'countryRegion': 'UK'}, exactly_one=True)

def test_geocode_postcode_invalid_postcode(mocked_geolocator):
    postcode = ''
    result = geocode_postcode(postcode)
    assert result is None
    mocked_geolocator.geocode.assert_not_called()

def test_geocode_postcode_geocode_timeout(mocked_geolocator):
    postcode = 'SW1A 2AA'
    mocked_geolocator.geocode.side_effect = GeocoderTimedOut()
    result = geocode_postcode(postcode)
    assert result is None
    mocked_geolocator.geocode.assert_called_once_with(query={'postalCode': postcode, 'countryRegion': 'UK'}, exactly_one=True)


def test_geocode_postcode_geocode_service_error(mocked_geolocator):
    postcode = 'SW1A 2AA'
    mocked_geolocator.geocode.side_effect = GeocoderServiceError()
    result = geocode_postcode(postcode)
    assert result is None
    mocked_geolocator.geocode.assert_called_once_with(query={'postalCode': postcode, 'countryRegion': 'UK'}, exactly_one=True)

def test_geocode_postcode_invalid_postcode_format(mocked_geolocator):
    postcode = 123
    result = geocode_postcode(postcode)
    assert result is None
    mocked_geolocator.geocode.assert_not_called()