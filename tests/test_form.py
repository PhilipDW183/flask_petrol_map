import pytest
from petrol_locations.forms import PetrolForm, FUEL_TYPES
from flask import Flask

@pytest.fixture
def app():
    app=Flask(__name__)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    return app

def test_postcode_valid(app):
    with app.app_context():
        form = PetrolForm(postcode="N19 4LD", fuel_type="E10")
        assert form.validate() is True

def test_postcode_invalid_characters(app):
    with app.app_context():
        form = PetrolForm(postcode="M1 $!%AA", fuel_type="Diesel")
        form.validate()
        assert "Not a recognised postcode" in form.postcode.errors

@pytest.mark.parametrize("postcode", ["M1", "M11", "M111", "M11111111", "M11111111"])
def test_postcode_invalid_length(app, postcode):
    with app.app_context():
        form = PetrolForm(postcode=postcode, fuel_type="Diesel")
        form.validate()
        assert "Should be 5 to 7 letters" in form.postcode.errors

@pytest.mark.parametrize("fuel", FUEL_TYPES)
def test_fuel_type_valid(app, fuel):
    with app.app_context():
        form = PetrolForm(postcode="M1 1AA", fuel_type=fuel)
        assert form.validate() is True

@pytest.mark.parametrize("fuel", ["Electric", "Oil", "Gas", "Petrol"])
def test_fuel_type_invalid(app, fuel):
    with app.app_context():
        form = PetrolForm(postcode="M1 1AA", fuel_type=fuel)
        form.validate()
        assert "Not a valid choice." in form.fuel_type.errors