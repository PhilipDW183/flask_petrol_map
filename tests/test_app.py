from petrol_locations import app
from flask.testing import FlaskClient
import pytest
from unittest.mock import MagicMock, patch

@pytest.fixture
def setup_app():
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    app.config["SECRET_KEY"] = "test"
    return app

@pytest.fixture
def mock_config():
    mock = MagicMock()
    with patch("petrol_locations.Config", return_value=mock):
        yield mock

def test_app_running(setup_app):
    with setup_app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200

def test_app_visible(setup_app):
    with setup_app.test_client() as client:
        response = client.get("/")
        assert b'Petrol station map' in response.data