import folium
import pytest
from petrol_locations.helpers import create_base_map, render_map

@pytest.fixture
def map_obj():
    return create_base_map()

def test_create_base_map():
    #test the default parameters
    map_obj=create_base_map()
    assert isinstance(map_obj, folium.Map)

    #test with custom parameters
    map_obj = create_base_map(longitude=40.712, latitude=74.060)
    assert isinstance(map_obj, folium.Map)

def test_render_map(map_obj):
    iframe = render_map(map_obj)
    assert isinstance(iframe, str)
    assert "<iframe srcdoc=" in iframe