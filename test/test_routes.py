def test_index_route(client):
    """Test that index route returns 200 and loads the custom UI."""
    response = client.get('/')
    assert response.status_code == 200
    # Check that key terms are present in the loaded HTML response
    assert b"Flask" in response.data
    assert b"Port" in response.data

def test_health_api(client):
    """Test that the /api/health route returns JSON and expected health fields."""
    response = client.get('/api/health')
    assert response.status_code == 200
    
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'Flask server is running on port 19191' in data['message']
    assert 'python_version' in data
    assert 'timestamp' in data

def test_feature1_route(client):
    """Test that the Morning Stock route returns 200 and loads stock page."""
    response = client.get('/feature1')
    assert response.status_code == 200
    assert b"2330.TW" in response.data
    assert b"NVDA" in response.data

def test_feature2_route(client):
    """Test that the Afternoon Workspace route returns 200 and loads company portal."""
    response = client.get('/feature2')
    assert response.status_code == 200
    assert b"punch-button" in response.data
    assert b"CKC_101" in response.data


