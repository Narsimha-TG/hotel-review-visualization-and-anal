from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
import os

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int = None
    hotel_name: str
    rating: int
    review_text: str
    sentiment: str = None

class ReviewCreate(BaseModel):
    hotel_name: str
    rating: int
    review_text: str

# In-memory database with sample data
reviews_db = [
    {"id": 1, "hotel_name": "Grand Plaza", "rating": 5, "review_text": "Fantastic service and stunning ocean views! Highly recommend.", "sentiment": "Positive"},
    {"id": 2, "hotel_name": "City Express", "rating": 2, "review_text": "Noisy rooms and poor room service. Will not stay again.", "sentiment": "Negative"},
    {"id": 3, "hotel_name": "Sunset Resort", "rating": 4, "review_text": "Great pool area and delicious breakfast options.", "sentiment": "Positive"},
    {"id": 4, "hotel_name": "Urban Hub", "rating": 3, "review_text": "Average stay, clean rooms but location is a bit far from downtown.", "sentiment": "Neutral"},
    {"id": 5, "hotel_name": "Grand Plaza", "rating": 1, "review_text": "Terrible experience, AC was broken and staff was rude.", "sentiment": "Negative"}
]

def analyze_sentiment(rating: int, text: str) -> str:
    text_lower = text.lower()
    positive_keywords = ["fantastic", "recommend", "great", "delicious", "wonderful", "amazing", "excellent"]
    negative_keywords = ["poor", "terrible", "noisy", "broken", "rude", "bad", "worst"]
    
    pos_score = sum(1 for word in positive_keywords if word in text_lower)
    neg_score = sum(1 for word in negative_keywords if word in text_lower)
    
    if rating >= 4 or pos_score > neg_score:
        return "Positive"
    elif rating <= 2 or neg_score > pos_score:
        return "Negative"
    else:
        return "Neutral"

@app.get("/api/reviews", response_model=List[Review])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", response_model=Review)
def create_review(review_in: ReviewCreate):
    new_id = max([r["id"] for r in reviews_db], default=0) + 1
    sentiment = analyze_sentiment(review_in.rating, review_in.review_text)
    new_review = {
        "id": new_id,
        "hotel_name": review_in.hotel_name,
        "rating": review_in.rating,
        "review_text": review_in.review_text,
        "sentiment": sentiment
    }
    reviews_db.insert(0, new_review)
    return new_review

@app.get("/api/dashboard")
def get_dashboard_stats():
    total_reviews = len(reviews_db)
    if total_reviews > 0:
        avg_rating = sum(r["rating"] for r in reviews_db) / total_reviews
    else:
        avg_rating = 0.0

    positive_count = sum(1 for r in reviews_db if r["sentiment"] == "Positive")
    neutral_count = sum(1 for r in reviews_db if r["sentiment"] == "Neutral")
    negative_count = sum(1 for r in reviews_db if r["sentiment"] == "Negative")

    rating_1 = sum(1 for r in reviews_db if r["rating"] == 1)
    rating_2 = sum(1 for r in reviews_db if r["rating"] == 2)
    rating_3 = sum(1 for r in reviews_db if r["rating"] == 3)
    rating_4 = sum(1 for r in reviews_db if r["rating"] == 4)
    rating_5 = sum(1 for r in reviews_db if r["rating"] == 5)

    stats = {
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
        "positive_count": positive_count,
        "neutral_count": neutral_count,
        "negative_count": negative_count,
        "rating_1": rating_1,
        "rating_2": rating_2,
        "rating_3": rating_3,
        "rating_4": rating_4,
        "rating_5": rating_5,
    }

    return {
        "stats": stats,
        "reviews": reviews_db
    }

@app.get("/")
def serve_index():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/index.html"))
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend index.html not found"}
