from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_get_reviews():
    response = client.get("/api/reviews")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 5

def test_create_review():
    payload = {
        "hotel_name": "Test Hotel",
        "reviewer_name": "John Doe",
        "rating": 5.0,
        "comment": "Outstanding stay!",
        "date": "2023-11-01"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["hotel_name"] == "Test Hotel"
    assert data["sentiment"] == "Positive"
    assert "id" in data

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert "average_rating" in data
    assert "sentiment_breakdown" in data
    assert "hotels" in data
