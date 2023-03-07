from petrol_locations import app
from flask.testing import FlaskClient

def test_app_running():
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

def test_app_visible():
    with app.test_client() as client:
        response = client.get("/")
        assert b'Petrol station map' in response.data