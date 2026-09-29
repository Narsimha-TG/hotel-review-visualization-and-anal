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
    assert len(response.json()) >= 2

def test_create_review():
    payload = {
        "hotel_name": "Mountain Lodge",
        "author": "Charlie Brown",
        "rating": 5,
        "comment": "Fantastic mountain views and cozy rooms.",
        "date": "2023-10-10"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["hotel_name"] == "Mountain Lodge"
    assert data["rating"] == 5

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert isinstance(data["total_reviews"], int)
