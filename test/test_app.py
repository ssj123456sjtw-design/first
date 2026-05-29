import pytest
from src import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app({"TESTING": True})
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


def test_feature1_success(client):
    """Test that feature1 successfully returns an image."""
    response = client.get("/feature1/sample.png")
    assert response.status_code == 200
    assert response.mimetype == "image/png"

def test_feature1_not_found(client):
    """Test that feature1 returns 404 for a missing image."""
    response = client.get("/feature1/nonexistent.png")
    assert response.status_code == 404

def test_feature2_success(client):
    """Test that feature2 successfully returns text file content."""
    response = client.get("/feature2/sample.txt")
    assert response.status_code == 200
    assert b"Hello from Flask!" in response.data
    assert response.mimetype == "text/plain"

def test_feature2_not_found(client):
    """Test that feature2 returns 404 for a missing text file."""
    response = client.get("/feature2/nonexistent.txt")
    assert response.status_code == 404

def test_feature2_invalid_extension(client):
    """Test that feature2 returns 404 for a file that is not .txt."""
    response = client.get("/feature2/sample.png")
    assert response.status_code == 404

def test_directory_traversal_prevention(client):
    """Test that directory traversal attempts are blocked or return 404/403."""
    response = client.get("/feature2/../images/sample.png")
    assert response.status_code in (403, 404)

def test_cpu_stress_endpoints(client):
    """Test that CPU stress endpoints work correctly (start, stop, status)."""
    # 1. Initially should be idle
    status_response = client.get("/api/cpu/stress/status")
    assert status_response.status_code == 200
    status_data = status_response.get_json()
    assert status_data["status"] == "idle"
    assert status_data["active_cores"] == 0

    try:
        # 2. Start stress test with 1 core for 5 seconds
        start_response = client.post(
            "/api/cpu/stress/start",
            json={"cores": 1, "duration": 5}
        )
        assert start_response.status_code == 200
        start_data = start_response.get_json()
        assert start_data["status"] == "success"
        assert "details" in start_data
        
        # 3. Check status is now stressing
        status_response = client.get("/api/cpu/stress/status")
        assert status_response.status_code == 200
        status_data = status_response.get_json()
        assert status_data["status"] == "stressing"
        assert status_data["active_cores"] == 1
        assert status_data["requested_cores"] == 1
        assert status_data["duration"] == 5

        # 4. Stop stress test
        stop_response = client.post("/api/cpu/stress/stop")
        assert stop_response.status_code == 200
        stop_data = stop_response.get_json()
        assert stop_data["status"] == "success"

        # 5. Check status is idle again
        status_response = client.get("/api/cpu/stress/status")
        status_data = status_response.get_json()
        assert status_data["status"] == "idle"
        assert status_data["active_cores"] == 0
    finally:
        # Cleanup processes in case of test failures
        client.post("/api/cpu/stress/stop")


