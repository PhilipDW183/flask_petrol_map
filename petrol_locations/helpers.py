import folium
from geopy.geocoders import Bing
from geopy.exc import GeocoderTimedOut, GeocoderServiceError
from flask_config import Config
import geopandas as gpd
from osmnx.geometries import geometries_from_point

CENTRAL_LONDON_LOC = [51.505, -0.09]
CONFIG = Config()


def create_base_map(
    longitude: float = CENTRAL_LONDON_LOC[0], latitude: float = CENTRAL_LONDON_LOC[1]
) -> folium.Map:
    """
    Generate a folium basemap

    Inputs
        longitude: longitude of location
        latitude: latitude of location

    Output
        Folium basemap of location
    """
    map_obj = folium.Map(location=[longitude, latitude], zoom_start=12)

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
            query={"postalCode": postcode, "countryRegion": "UK"}, exactly_one=True
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


def get_surrounding_petrol_stations(
    center_point: list, fuel_type: str, distance: int = 2_000
):
    """
    get petrol stations around a central point

    Inputs
        centre_point: (lat, lon) from which to search around
        distance: distance in metres to search around centre point

    Outputs:
        petrol_locations: geoDataFrame of petrol locations or None
    """

    try:
        if not all(
            isinstance(point, float) for point in center_point
        ) or not isinstance(distance, int):
            raise ValueError("Incorrect values passed")

        petrol_locations = geometries_from_point(
            center_point=center_point,
            tags={"amenity": "fuel", "fuel": fuel_type},
            dist=distance,
        )

        if (
            not isinstance(petrol_locations, gpd.GeoDataFrame)
            or len(petrol_locations) < 1
        ):
            raise TypeError("No petrol locations found")

        return petrol_locations

    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)


def add_petrol_stations_to_map(
    map_obj: folium.Map, gdf: gpd.GeoDataFrame, popup_text_col: list = None
):
    """
    Add points from a GeoDataFrame to a Folium Map object

    Inputs
        map_obj: A Folium Map Object
        gdf: A GeoDataFrame containing point geometries
        popup_text_col: A string representing the column name containg the popup text

    Outputs
        map_obj: A Folium Map Object with markers
    """
    try:
        if not isinstance(map_obj, folium.Map) or not isinstance(gdf, gpd.GeoDataFrame):
            raise ValueError("Invalid map or geodataframe")

        if popup_text_col and not any(col in popup_text_col for col in gdf.columns):
            raise ValueError(f"{popup_text_col} not found in GeoDataFrame columns")

        if "geometry" not in gdf.columns:
            raise ValueError("No 'geometry' column found in GeoDataFrame")

        gdf = convert_polygons_to_points(gdf)

        popup_valid_text_cols = [col for col in popup_text_col if col in gdf.columns]

        popup_text = get_petrol_stations_name(gdf, popup_valid_text_cols)

        tooltip = "Petrol Station"

        for coord, text in zip(gdf.geometry, popup_text):
            folium.Marker(
                location=[coord.y, coord.x],
                popup=text,
                tooltip=tooltip,
                icon=folium.Icon(color="blue", icon="gas-pump", prefix="fa"),
            ).add_to(map_obj)

        return map_obj

    except ValueError as e:
        print(e)
    except Exception as e:
        print(e)


def convert_polygons_to_points(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Converts all polygons in a geodataframe to points
    """
    gdf["geometry"] = gdf["geometry"].centroid

    return gdf


def add_origin_to_map(
    latitude: float, longitude: float, map_obj: folium.Map
) -> folium.Map:
    """
    Add origin to the folium map object

    Inputs
        latitude: float of latitude
        longitude: float of longitude
        map_obj: folium map object to add the marker to
    
    Outputs
        map_obj: folium Map obejct with marker for origin
    """
    folium.Marker(
        location=[latitude, longitude],
        popup="Home",
        tooltip="Home",
        icon=folium.Icon(color="red", icon="home", prefix="fa"),
    ).add_to(map_obj)

    return map_obj


def add_circle_to_map(
    latitude: float, longitude: float, map_obj: folium.Map, distance: int
) -> folium.Map:
    """
    Adds distance circle to map

      Inputs
        latitude: float of latitude
        longitude: float of longitude
        map_obj: folium map object to add the marker to
    
    Outputs
        map_obj: folium Map obejct with origin circle added
    """

    folium.Circle(
        radius=distance,
        location=[latitude, longitude],
        popup=f"Distance: {distance/1000}km",
        color="crimson",
        fill=False,
    ).add_to(map_obj)

    return map_obj

def get_petrol_stations_name(gdf: gpd.GeoDataFrame, columns: list) -> list:
    """
    Gets the name of the petrol station

    Inputs
        gdf: GeoDataFrame of petrol station names
        columns: list of columns containing potential names order by preference

    Outputs:
        petrol_names: list of names of names of petrol station
    """

    petrol_names = []

    for index, row in gdf.iterrows():
        petrol_station_names = row[columns]
        petrol_station_name_col = petrol_station_names.first_valid_index()
        petrol_station_name = petrol_station_names[petrol_station_name_col]
        petrol_names.append(petrol_station_name)

    return petrol_names