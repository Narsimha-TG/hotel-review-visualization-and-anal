from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import uuid
import os

app = FastAPI(
    title="Hotel Review Visualization and Analysis Dashboard",
    description="API for managing and analyzing hotel reviews with sentiment insights.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic Models
class ReviewCreate(BaseModel):
    hotel_name: str = Field(..., description="Name of the hotel")
    reviewer_name: str = Field(..., description="Name of the reviewer")
    rating: int = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: str = Field(..., description="Review comment text")

class ReviewUpdate(BaseModel):
    hotel_name: Optional[str] = None
    reviewer_name: Optional[str] = None
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None

class Review(BaseModel):
    id: str
    hotel_name: str
    reviewer_name: str
    rating: int
    comment: str
    sentiment: str

# Helper function for rule-based sentiment analysis
def analyze_sentiment(rating: int, comment: str) -> str:
    comment_lower = comment.lower()
    positive_keywords = ["great", "excellent", "amazing", "wonderful", "fantastic", "clean", "friendly", "perfect", "best", "loved", "comfortable", "spacious"]
    negative_keywords = ["terrible", "awful", "bad", "poor", "dirty", "rude", "worst", "disappointing", "noisy", "slow", "uncomfortable", "broken"]
    
    pos_score = sum(1 for kw in positive_keywords if kw in comment_lower)
    neg_score = sum(1 for kw in negative_keywords if kw in comment_lower)
    
    if rating >= 4 or (pos_score > neg_score and rating >= 3):
        return "Positive"
    elif rating <= 2 or (neg_score > pos_score):
        return "Negative"
    else:
        return "Neutral"

# In-memory database initialized with realistic seed reviews
reviews_db = [
    {
        "id": "rev-101",
        "hotel_name": "Grand Plaza Resort",
        "reviewer_name": "Alice Smith",
        "rating": 5,
        "comment": "Fantastic stay! The room was extremely clean and the staff was very friendly and helpful. Highly recommended!",
        "sentiment": "Positive"
    },
    {
        "id": "rev-102",
        "hotel_name": "Grand Plaza Resort",
        "reviewer_name": "Bob Jones",
        "rating": 2,
        "comment": "A bit disappointing. The room was noisy and the air conditioning was broken throughout the night.",
        "sentiment": "Negative"
    },
    {
        "id": "rev-103",
        "hotel_name": "Seaside Paradise Hotel",
        "reviewer_name": "Charlie Brown",
        "rating": 4,
        "comment": "Wonderful ocean view and comfortable beds. Breakfast was delicious, though service at the front desk was a bit slow.",
        "sentiment": "Positive"
    },
    {
        "id": "rev-104",
        "hotel_name": "Urban Boutique Inn",
        "reviewer_name": "Diana Prince",
        "rating": 3,
        "comment": "Average hotel for a short business trip. Location is great, but the rooms are quite small and basic.",
        "sentiment": "Neutral"
    },
    {
        "id": "rev-105",
        "hotel_name": "Seaside Paradise Hotel",
        "reviewer_name": "Ethan Hunt",
        "rating": 1,
        "comment": "Terrible experience. The room was dirty and the staff was completely rude when we asked for fresh towels.",
        "sentiment": "Negative"
    }
]

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend_path):
        with open(frontend_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>Dashboard frontend not found</h1>"

@app.get("/api/reviews", response_list=List[Review])
async def get_reviews(
    search: Optional[str] = Query(None, description="Search query for comment or hotel name"),
    sentiment: Optional[str] = Query(None, description="Filter by sentiment"),
    hotel_name: Optional[str] = Query(None, description="Filter by hotel name")
):
    filtered = reviews_db
    if search:
        q = search.lower()
        filtered = [r for r in filtered if q in r["hotel_name"].lower() or q in r["comment"].lower() or q in r["reviewer_name"].lower()]
    if sentiment:
        filtered = [r for r in filtered if r["sentiment"].lower() == sentiment.lower()]
    if hotel_name:
        filtered = [r for r in filtered if r["hotel_name"].lower() == hotel_name.lower()]
    return filtered

@app.get("/api/reviews/{review_id}", response_model=Review)
async def get_review(review_id: str):
    for r in reviews_db:
        if r["id"] == review_id:
            return r
    raise HTTPException(status_code=404, detail="Review not found")

@app.post("/api/reviews", response_model=Review, status_code=201)
async def create_review(payload: ReviewCreate):
    new_id = f"rev-{uuid.uuid4().hex[:6]}"
    sentiment = analyze_sentiment(payload.rating, payload.comment)
    new_review = {
        "id": new_id,
        "hotel_name": payload.hotel_name,
        "reviewer_name": payload.reviewer_name,
        "rating": payload.rating,
        "comment": payload.comment,
        "sentiment": sentiment
    }
    reviews_db.insert(0, new_review)
    return new_review

@app.put("/api/reviews/{review_id}", response_model=Review)
async def update_review(review_id: str, payload: ReviewUpdate):
    for r in reviews_db:
        if r["id"] == review_id:
            if payload.hotel_name is not None:
                r["hotel_name"] = payload.hotel_name
            if payload.reviewer_name is not None:
                r["reviewer_name"] = payload.reviewer_name
            if payload.rating is not None:
                r["rating"] = payload.rating
            if payload.comment is not None:
                r["comment"] = payload.comment
            # Re-calculate sentiment if rating or comment changed
            r["sentiment"] = analyze_sentiment(r["rating"], r["comment"])
            return r
    raise HTTPException(status_code=404, detail="Review not found")

@app.delete("/api/reviews/{review_id}", status_code=204)
async def delete_review(review_id: str):
    global reviews_db
    for idx, r in enumerate(reviews_db):
        if r["id"] == review_id:
            reviews_db.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Review not found")

@app.get("/api/stats")
async def get_stats():
    total = len(reviews_db)
    if total == 0:
        return {
            "total_reviews": 0,
            "average_rating": 0.0,
            "positive_percentage": 0.0,
            "negative_percentage": 0.0
        }
    
    avg_rating = sum(r["rating"] for r in reviews_db) / total
    pos_count = sum(1 for r in reviews_db if r["sentiment"] == "Positive")
    neg_count = sum(1 for r in reviews_db if r["sentiment"] == "Negative")
    
    return {
        "total_reviews": total,
        "average_rating": round(avg_rating, 2),
        "positive_percentage": round((pos_count / total) * 100, 1),
        "negative_percentage": round((neg_count / total) * 100, 1)
    }

@app.get("/api/hotels")
async def get_hotels():
    hotels = sorted(list(set(r["hotel_name"] for r in reviews_db)))
    return hotels

@app.get("/api/analytics/charts")
async def get_chart_analytics():
    # Sentiment breakdown
    pos = sum(1 for r in reviews_db if r["sentiment"] == "Positive")
    neu = sum(1 for r in reviews_db if r["sentiment"] == "Neutral")
    neg = sum(1 for r in reviews_db if r["sentiment"] == "Negative")

    # Rating distribution
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reviews_db:
        if r["rating"] in rating_counts:
            rating_counts[r["rating"]] += 1

    # Aspect mock ratings
    aspects = {
        "Cleanliness": 4.2,
        "Staff & Service": 4.0,
        "Location": 4.6,
        "Value for Money": 3.8,
        "Comfort": 4.1
    }

    return {
        "sentiment_breakdown": {
            "labels": ["Positive", "Neutral", "Negative"],
            "counts": [pos, neu, neg]
        },
        "rating_distribution": {
            "labels": ["1 Star", "2 Stars", "3 Stars", "4 Stars", "5 Stars"],
            "counts": [rating_counts[1], rating_counts[2], rating_counts[3], rating_counts[4], rating_counts[5]]
        },
        "aspect_ratings": {
            "labels": list(aspects.keys()),
            "scores": list(aspects.values())
        }
    }
