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

def test_create_and_filter_review():
    payload = {
        "hotel_name": "Test Hotel",
        "author": "Tester",
        "rating": 5,
        "comment": "Outstanding experience!",
        "date": "2023-11-01"
    }
    response = client.post("/api/reviews", json=payload)
    assert response.status_code == 201
    created = response.json()
    assert created["hotel_name"] == "Test Hotel"
    assert created["sentiment"] == "Positive"

    # Test filtering by hotel
    filtered_resp = client.get("/api/reviews?hotel=Test Hotel")
    assert filtered_resp.status_code == 200
    f_data = filtered_resp.json()
    assert len(f_data) == 1
    assert f_data[0]["author"] == "Tester"

def test_analytics():
    response = client.get("/api/analytics")
    assert response.status_code == 200
    data = response.json()
    assert "total_reviews" in data
    assert "average_rating" in data
    assert "sentiment_breakdown" in data
    assert "hotel_summaries" in data
    assert data["total_reviews"] > 0
