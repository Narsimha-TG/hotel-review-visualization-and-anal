import pytest
from fastapi.testclient import TestClient
from main import app, reset_data

client = TestClient(app)

@pytest.fixture(autouse=True)
def reset_state():
    reset_data()
    yield

def test_health():
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_get_hotels():
    response = client.get("/api/hotels")
    assert response.status_code == 200
    hotels = response.json()
    assert len(hotels) >= 3
    assert any(h["id"] == "grand-palace" for h in hotels)

def test_get_overview():
    response = client.get("/api/overview?hotel_id=grand-palace")
    assert response.status_code == 200
    data = response.json()
    assert data["total_reviews"] == 6
    assert data["average_rating"] > 0
    assert "net_sentiment_score" in data
    assert "sentiment_distribution" in data
    assert data["sentiment_distribution"]["positive"] >= 1

def test_get_aspects():
    response = client.get("/api/aspects?hotel_id=grand-palace")
    assert response.status_code == 200
    data = response.json()
    assert "cleanliness" in data["aspects"]
    assert "benchmarks" in data
    assert 1.0 <= data["aspects"]["cleanliness"] <= 5.0

def test_get_trends():
    response = client.get("/api/trends?hotel_id=grand-palace")
    assert response.status_code == 200
    trends = response.json()
    assert isinstance(trends, list)
    assert len(trends) > 0
    assert "average_rating" in trends[0]

def test_get_keywords():
    response = client.get("/api/keywords")
    assert response.status_code == 200
    keywords = response.json()
    assert isinstance(keywords, list)
    if len(keywords) > 0:
        assert "keyword" in keywords[0]
        assert "frequency" in keywords[0]

def test_get_reviews_filter():
    response = client.get("/api/reviews?hotel_id=grand-palace&sentiment=positive")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    for rev in data["reviews"]:
        assert rev["sentiment"] == "positive"

def test_post_review():
    new_review_payload = {
        "hotel_id": "grand-palace",
        "author_name": "Alex Rivera",
        "rating": 5.0,
        "title": "Unbelievable experience and wonderful staff!",
        "comment": "Amazing views, clean pool, delicious cocktails, top notch concierge!",
        "stay_type": "Couple",
        "room_type": "Oceanfront Suite",
        "aspects": {
            "cleanliness": 5.0,
            "service": 5.0,
            "location": 5.0,
            "value": 4.0,
            "amenities": 5.0,
            "dining": 5.0
        }
    }
    response = client.post("/api/reviews", json=new_review_payload)
    assert response.status_code == 201
    created = response.json()
    assert created["id"] is not None
    assert created["sentiment"] == "positive"
    assert created["author_name"] == "Alex Rivera"
    
    # Verify it now appears in overview total count
    overview_resp = client.get("/api/overview?hotel_id=grand-palace")
    assert overview_resp.json()["total_reviews"] == 7
