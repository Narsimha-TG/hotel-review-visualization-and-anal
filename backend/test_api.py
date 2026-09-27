from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_reviews():
    response = client.get("/api/reviews")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    assert "total_reviews" in response.json()
