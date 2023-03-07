from petrol_locations import app

@app.route("/")
def index():
    return "<h1>Hello World</h1>"