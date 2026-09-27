from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

# Mock dataset for hotel reviews
MOCK_REVIEWS = [
    {"id": 1, "hotel_name": "Grand Plaza", "reviewer_name": "Alice Smith", "rating": 5, "comment": "Exceptional service and wonderful rooms! Truly enjoyed our stay.", "sentiment": "Positive"},
    {"id": 2, "hotel_name": "Ocean Breeze", "reviewer_name": "Bob Jones", "rating": 2, "comment": "The room was dirty and the staff was extremely unhelpful.", "sentiment": "Negative"},
    {"id": 3, "hotel_name": "Mountain View", "reviewer_name": "Charlie Brown", "rating": 4, "comment": "Great location and nice views, but breakfast was mediocre.", "sentiment": "Neutral"},
    {"id": 4, "hotel_name": "Grand Plaza", "reviewer_name": "Diana Prince", "rating": 5, "comment": "Luxury at its finest. Will definitely come back again.", "sentiment": "Positive"},
    {"id": 5, "hotel_name": "City Express", "reviewer_name": "Evan Wright", "rating": 3, "comment": "Average hotel. Good for a quick overnight stay.", "sentiment": "Neutral"},
    {"id": 6, "hotel_name": "Ocean Breeze", "reviewer_name": "Fiona Gallagher", "rating": 1, "comment": "Terrible experience. Loud noise all night long.", "sentiment": "Negative"},
    {"id": 7, "hotel_name": "Mountain View", "reviewer_name": "George Clark", "rating": 5, "comment": "Breathtaking scenery and immaculate hospitality.", "sentiment": "Positive"}
]

@app.get("/api/dashboard")
def get_dashboard_data():
    total_reviews = len(MOCK_REVIEWS)
    avg_rating = sum(r["rating"] for r in MOCK_REVIEWS) / total_reviews if total_reviews > 0 else 0
    
    sentiments = [r["sentiment"] for r in MOCK_REVIEWS]
    pos_count = sentiments.count("Positive")
    neg_count = sentiments.count("Negative")
    neu_count = sentiments.count("Neutral")
    
    positive_percentage = round((pos_count / total_reviews) * 100, 1) if total_reviews > 0 else 0
    negative_percentage = round((neg_count / total_reviews) * 100, 1) if total_reviews > 0 else 0

    rating_distribution = {
        "1 Star": sum(1 for r in MOCK_REVIEWS if r["rating"] == 1),
        "2 Stars": sum(1 for r in MOCK_REVIEWS if r["rating"] == 2),
        "3 Stars": sum(1 for r in MOCK_REVIEWS if r["rating"] == 3),
        "4 Stars": sum(1 for r in MOCK_REVIEWS if r["rating"] == 4),
        "5 Stars": sum(1 for r in MOCK_REVIEWS if r["rating"] == 5),
    }

    sentiment_distribution = {
        "Positive": pos_count,
        "Negative": neg_count,
        "Neutral": neu_count
    }

    return {
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "rating_distribution": rating_distribution,
        "sentiment_distribution": sentiment_distribution,
        "recent_reviews": MOCK_REVIEWS[::-1]
    }

@app.get("/")
def serve_index():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Frontend index.html not found</h1>", status_code=404)
