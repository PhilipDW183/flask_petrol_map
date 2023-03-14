from petrol_locations.helpers import geocode_postcode, get_surrounding_petrol_stations, add_petrol_stations_to_map
from unittest.mock import MagicMock, patch
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from geopandas import GeoDataFrame
import geopandas as gpd
from shapely.geometry import Point
import pytest
import folium

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


def test_get_surrounding_petrol_stations_valid_response():
    mock_data = {'name': ['Point A', 'Point B'], 'geometry': [Point(0, 0), Point(1, 1)]}
    mock_gdf = GeoDataFrame(mock_data, crs='epsg:4326')
    with patch("petrol_locations.helpers.geometries_from_point", return_value = mock_gdf):
        center_point = (-0.13329, 51.54558)
        distance = 2_000
        result = get_surrounding_petrol_stations(center_point, distance)
        assert result is not None
        assert len(result) > 0

def test_get_surrounding_petrol_stations_invalid_response():
    with patch("petrol_locations.helpers.geometries_from_point", return_value = None):
        center_point = (-0.13329, 51.54558)
        distance = 2_000
        result = get_surrounding_petrol_stations(center_point, distance)
        assert result == None

@pytest.mark.parametrize("point, distance", 
                         [((-0.13329, 51.54558), "distance"), 
                          ((None, 51.54558), 1000), 
                          ((-0.13329, None), 1000)])
def test_get_surrounding_petrol_stations_invalid_input(point, distance):
    result = get_surrounding_petrol_stations(point, distance)
    assert result == None


@pytest.fixture
def map_obj():
    return folium.Map(location=[51.5074, 0.1278], zoom_start=12)

@pytest.fixture
def petrol_stations_gdf():
    points = [Point(0.1, 51.5), Point(0.2, 51.5), Point(0.3, 51.5)]
    data = {'geometry': points, 'name': ['Station 1', 'Station 2', 'Station 3']}
    gdf = gpd.GeoDataFrame(data)
    return gdf


def test_add_petrol_stations_to_map_with_valid_input(map_obj, petrol_stations_gdf):
    # Call the function with valid input parameters
    result = add_petrol_stations_to_map(map_obj, petrol_stations_gdf, ["name"])

    # Check that the result is a Folium Map object with markers
    assert isinstance(result, folium.Map)


def test_add_petrol_stations_to_map_with_invalid_input(map_obj, petrol_stations_gdf):
    # Call the function with invalid input parameters
    result = add_petrol_stations_to_map(None, petrol_stations_gdf, ["name"])
    assert result == None

    result = add_petrol_stations_to_map(map_obj, None, ["name"])
    assert result == None

    result = add_petrol_stations_to_map(map_obj, petrol_stations_gdf)
    assert result == None




def test_add_petrol_stations_to_map_with_missing_geometry_column(map_obj):
    # Create a GeoDataFrame without a 'geometry' column
    data = {'name': ['Station 1', 'Station 2', 'Station 3']}
    gdf = gpd.GeoDataFrame(data)

    result = add_petrol_stations_to_map(map_obj, gdf, ["name"])
    assert result == None

