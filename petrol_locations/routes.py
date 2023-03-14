from petrol_locations import app
from petrol_locations.forms import PetrolForm
from petrol_locations.helpers import (
    create_base_map,
    render_map,
    geocode_postcode,
    get_surrounding_petrol_stations,
    add_petrol_stations_to_map,
    add_circle_to_map,
    add_origin_to_map
)
from flask import render_template, flash
import geopandas as gpd

DISTANCE = 2_000


@app.route("/", methods=["GET", "POST"])
def index():
    form = PetrolForm()
    map_obj = create_base_map()
    iframe = render_map(map_obj)
    if form.validate_on_submit():
        print("validated")
        postcode = form.postcode.data
        fuel_type = form.fuel_type.data
        location = geocode_postcode(postcode)
        if not location:
            flash("Postcode not found", "danger")
            return render_template("index.html", form=form, map=iframe)
        
        petrol_stores = get_surrounding_petrol_stations(
            center_point=(location[1], location[0]), distance=DISTANCE,
            fuel_type=fuel_type
        )

        if not isinstance(petrol_stores, gpd.GeoDataFrame):
            flash("No petrol stations found nearby", "danger")
            petrol_map = create_base_map(location[1], location[0])
            petrol_map = add_origin_to_map(location[1], location[0], petrol_map)
            iframe = render_map(petrol_map)
            return render_template("index.html", form=form, map=iframe)
        
        petrol_map = create_base_map(location[1], location[0])
        petrol_map = add_petrol_stations_to_map(petrol_map, petrol_stores, "name")
        petrol_map = add_origin_to_map(location[1], location[0], petrol_map)
        petrol_map = add_circle_to_map(location[1], location[0], petrol_map, DISTANCE+500)
        iframe = render_map(petrol_map)
        return render_template("index.html", form=form, map=iframe)

    return render_template("index.html", form=form, map=iframe)