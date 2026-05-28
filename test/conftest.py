import pytest
from src import create_app
from src.config import Config

class TestConfig(Config):
    TESTING = True
    DEBUG = False

@pytest.fixture
def app():
    """Fixture for creating a test application instance."""
    app = create_app(TestConfig)
    yield app

@pytest.fixture
def client(app):
    """Fixture for getting a test client."""
    return app.test_client()
