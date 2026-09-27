from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "Welcome" in response.json()["message"]

def test_get_reviews():
    response = client.get("/api/reviews")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert "avg_rating" in data
    assert "sentiment_breakdown" in data

def test_create_review():
    payload = {
        "hotel_name": "Test Hotel",
        "city": "Chicago",
        "rating": 5,
        "review_text": "Phenomenal stay!"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["hotel_name"] == "Test Hotel"
    assert data["sentiment"] == "Positive"
