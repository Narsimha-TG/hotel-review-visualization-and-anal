from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import os

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

# In-memory database with initial sample reviews
REVIEWS_DB = [
    {
        "id": "rev-1",
        "hotel_name": "Grand Plaza Hotel",
        "rating": 5,
        "review_text": "Absolutely wonderful stay! The staff were extremely helpful, rooms were spotless, and the breakfast buffet was delicious.",
        "sentiment": "Positive",
        "author": "Sarah Jenkins"
    },
    {
        "id": "rev-2",
        "hotel_name": "Grand Plaza Hotel",
        "rating": 2,
        "review_text": "Disappointing experience. The air conditioning was broken for half our stay and front desk ignored our complaints.",
        "sentiment": "Negative",
        "author": "Michael Chang"
    },
    {
        "id": "rev-3",
        "hotel_name": "Ocean View Resort",
        "rating": 4,
        "review_text": "Great beachside location and stunning sunset views. Rooms are a bit dated but very clean.",
        "sentiment": "Positive",
        "author": "Emma Watson"
    },
    {
        "id": "rev-4",
        "hotel_name": "Ocean View Resort",
        "rating": 3,
        "review_text": "Average hotel. Nothing special. Food at the restaurant was mediocre and overpriced.",
        "sentiment": "Neutral",
        "author": "David Miller"
    },
    {
        "id": "rev-5",
        "hotel_name": "Mountain Lodge & Spa",
        "rating": 5,
        "review_text": "Incredible mountain retreat! The spa treatments were world-class and the fireplace in the suite was very cozy.",
        "sentiment": "Positive",
        "author": "Jessica Taylor"
    },
    {
        "id": "rev-6",
        "hotel_name": "Urban Express Inn",
        "rating": 1,
        "review_text": "Terrible noise from the street all night long. Bed was uncomfortable and Wi-Fi did not work at all.",
        "sentiment": "Negative",
        "author": "Robert Downey"
    }
]

class ReviewCreate(BaseModel):
    hotel_name: str
    rating: int = Field(..., ge=1, le=5)
    review_text: str
    author: Optional[str] = "Anonymous"

class Review(ReviewCreate):
    id: str
    sentiment: str

def analyze_sentiment(rating: int, text: str) -> str:
    text_lower = text.lower()
    positive_keywords = ["wonderful", "great", "excellent", "amazing", "fantastic", "spotless", "delicious", "helpful", "stunning", "cozy", "world-class", "love"]
    negative_keywords = ["disappointing", "broken", "ignored", "mediocre", "overpriced", "terrible", "noise", "uncomfortable", "bad", "horrible", "poor"]
    
    pos_score = sum(1 for w in positive_keywords if w in text_lower)
    neg_score = sum(1 for w in negative_keywords if w in text_lower)
    
    if rating >= 4 or pos_score > neg_score:
        return "Positive"
    elif rating <= 2 or neg_score > pos_score:
        return "Negative"
    else:
        return "Neutral"

@app.get("/api/hotels", response_model=List[str])
def get_hotels():
    hotels = sorted(list(set(r["hotel_name"] for r in REVIEWS_DB)))
    return hotels

@app.get("/api/reviews", response_model=List[Review])
def get_reviews(
    hotel: Optional[str] = None,
    sentiment: Optional[str] = None,
    search: Optional[str] = None
):
    filtered = REVIEWS_DB
    if hotel and hotel != "ALL":
        filtered = [r for r in filtered if r["hotel_name"].lower() == hotel.lower()]
    if sentiment and sentiment != "ALL":
        filtered = [r for r in filtered if r["sentiment"].lower() == sentiment.lower()]
    if search:
        q = search.lower()
        filtered = [r for r in filtered if q in r["review_text"].lower() or q in r["hotel_name"].lower() or q in r["author"].lower()]
    return filtered

@app.post("/api/reviews", response_model=Review)
def create_review(payload: ReviewCreate):
    sentiment = analyze_sentiment(payload.rating, payload.review_text)
    new_rev = {
        "id": f"rev-{uuid.uuid4().hex[:8]}",
        "hotel_name": payload.hotel_name,
        "rating": payload.rating,
        "review_text": payload.review_text,
        "sentiment": sentiment,
        "author": payload.author or "Anonymous"
    }
    REVIEWS_DB.insert(0, new_rev)
    return new_rev

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: str):
    global REVIEWS_DB
    initial_len = len(REVIEWS_DB)
    REVIEWS_DB = [r for r in REVIEWS_DB if r["id"] != review_id]
    if len(REVIEWS_DB) == initial_len:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"status": "success", "message": "Review deleted"}

@app.get("/api/stats")
def get_stats(hotel: Optional[str] = None):
    target_reviews = REVIEWS_DB
    if hotel and hotel != "ALL":
        target_reviews = [r for r in target_reviews if r["hotel_name"].lower() == hotel.lower()]
    
    total = len(target_reviews)
    if total == 0:
        return {
            "total_reviews": 0,
            "avg_rating": 0.0,
            "positive_percentage": 0.0,
            "negative_percentage": 0.0,
            "neutral_percentage": 0.0,
            "rating_counts": {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0},
            "sentiment_counts": {"Positive": 0, "Neutral": 0, "Negative": 0}
        }
    
    avg_rating = sum(r["rating"] for r in target_reviews) / total
    
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for r in target_reviews:
        s = r["sentiment"]
        if s in sentiment_counts:
            sentiment_counts[s] += 1
            
    rating_counts = {"1": 0, "2": 0, "3": 0, "4": 0, "5": 0}
    for r in target_reviews:
        rating_counts[str(r["rating"])] += 1
        
    pos_pct = (sentiment_counts["Positive"] / total) * 100
    neg_pct = (sentiment_counts["Negative"] / total) * 100
    neu_pct = (sentiment_counts["Neutral"] / total) * 100
    
    return {
        "total_reviews": total,
        "avg_rating": avg_rating,
        "positive_percentage": pos_pct,
        "negative_percentage": neg_pct,
        "neutral_percentage": neu_pct,
        "rating_counts": rating_counts,
        "sentiment_counts": sentiment_counts
    }

@app.get("/")
def serve_frontend():
    frontend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../frontend/index.html"))
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return HTMLResponse("<h3>Frontend index.html not found</h3>", status_code=404)
