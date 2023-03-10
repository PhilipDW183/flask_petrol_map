import folium

CENTRAL_LONDON_LOC = [51.505, -0.09]

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