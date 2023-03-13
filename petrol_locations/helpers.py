import folium
from geopy.geocoders import Bing
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from flask_config import Config

CENTRAL_LONDON_LOC = [51.505, -0.09]
CONFIG = Config()

def create_base_map(longitude: float = CENTRAL_LONDON_LOC[0],
                     latitude: float = CENTRAL_LONDON_LOC[1]) -> folium.Map:
    """
    Generate a folium basemap 

    Inputs
        longitude: longitude of location
        latitude: latitude of location

    Output
        Folium basemap of location
    """
    map_obj = folium.Map(location=[longitude, latitude],
                     zoom_start=12)
    
    return map_obj

def render_map(map_obj: folium.Map):
    """
    Generate iframe of folium map object

    Inputs
        map: folium map object

    Outputs
        iframe: iframe of folium map object to embed in web app
    """

    iframe = map_obj.get_root()._repr_html_()

    return iframe

def geocode_postcode(postcode: str) -> tuple:
    """
    Turn the postcode into a longitude and latitude point

    Inputs
        postocde: postocde for the UK

    Outputs
        point: longitude and latitude as a tuple (longitude, latitude) else None
    """
    try:

        if not postcode or not isinstance(postcode, str):
            raise ValueError("Invalid postcode format")
        geolocator = Bing(api_key=CONFIG.BING_API_KEY)

        point_location = geolocator.geocode(
                query={"postalCode":postcode,
                        "countryRegion":"UK"},
                exactly_one=True
        )

        if point_location:
            point = (point_location.longitude, point_location.latitude)
        else:
            point = None

        return point
    
    except (GeocoderTimedOut, GeocoderServiceError) as e:
        print(f"Error geocoding postcode {postcode}: {e}")
        return None
    except ValueError as e:
        print(e)
        return None