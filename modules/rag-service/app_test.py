import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_endpoint(client):
    """Test if the /health endpoint returns status OK."""
    response = client.get('/health')
    assert response.status_code == 200
    json_data = response.get_json()
    assert json_data['message'] == "OK", "Health check message is not OK"