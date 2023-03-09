from petrol_locations import app
from petrol_locations.forms import PetrolForm
from flask import render_template

@app.route("/")
def index():
    form = PetrolForm()
    return render_template("index.html", form=form)