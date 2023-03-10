from petrol_locations import app
from petrol_locations.forms import PetrolForm
from petrol_locations.helpers import create_base_map, render_map
from flask import render_template

@app.route("/")
def index():
    form = PetrolForm()
    map_obj = create_base_map()
    iframe = render_map(map_obj)
    return render_template("index.html", form=form, map=iframe)