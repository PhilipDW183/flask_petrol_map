from petrol_locations import app
from petrol_locations.forms import PetrolForm
from petrol_locations.helpers import create_base_map, render_map, geocode_postcode
from flask import render_template, flash

@app.route("/", methods=["GET", "POST"])
def index():
    form = PetrolForm()
    map_obj = create_base_map()
    iframe = render_map(map_obj)
    if form.validate_on_submit():
        postcode = form.postcode.data
        fuel_type = form.fuel_type.data
        location = geocode_postcode(postcode)
        if not location:
            flash("Postcode not found", "danger")
            render_template("index.html", form=form, map=iframe)
        else:
            render_template("index.html", form=form, map=iframe)
    return render_template("index.html", form=form, map=iframe)