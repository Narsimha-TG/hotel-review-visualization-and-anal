from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock Database / Dataset
REVIEWS_DB = [
    {
        "id": 1,
        "hotel_name": "Grand Palace Hotel",
        "city": "New York",
        "rating": 5,
        "sentiment": "Positive",
        "review_text": "Exceptional service and breathtaking views of the city skyline. Will definitely return!",
        "date": "2023-10-15"
    },
    {
        "id": 2,
        "hotel_name": "Grand Palace Hotel",
        "city": "New York",
        "rating": 2,
        "sentiment": "Negative",
        "review_text": "The room was extremely noisy and the air conditioning was broken all night.",
        "date": "2023-10-18"
    },
    {
        "id": 3,
        "hotel_name": "Seaside Resort & Spa",
        "city": "Miami",
        "rating": 4,
        "sentiment": "Positive",
        "review_text": "Wonderful beachfront location, great cocktails at the pool bar, friendly staff.",
        "date": "2023-11-02"
    },
    {
        "id": 4,
        "hotel_name": "Seaside Resort & Spa",
        "city": "Miami",
        "rating": 3,
        "sentiment": "Neutral",
        "review_text": "Average experience. Food at the buffet was mediocre for the price paid.",
        "date": "2023-11-05"
    },
    {
        "id": 5,
        "hotel_name": "Alpine Lodge",
        "city": "Denver",
        "rating": 5,
        "sentiment": "Positive",
        "review_text": "Cozy fireplace, incredible mountain proximity, and top-notch hot chocolate.",
        "date": "2023-12-01"
    },
    {
        "id": 6,
        "hotel_name": "Alpine Lodge",
        "city": "Denver",
        "rating": 1,
        "sentiment": "Negative",
        "review_text": "Terrible customer service at the front desk when checking in. Lost our reservation.",
        "date": "2023-12-10"
    },
    {
        "id": 7,
        "hotel_name": "Urban Boutique",
        "city": "San Francisco",
        "rating": 4,
        "sentiment": "Positive",
        "review_text": "Charming interior design, very walkable neighborhood, excellent coffee maker in room.",
        "date": "2024-01-12"
    },
    {
        "id": 8,
        "hotel_name": "Urban Boutique",
        "city": "San Francisco",
        "rating": 3,
        "sentiment": "Neutral",
        "review_text": "Rooms are a bit small but clean. Parking garage is extremely tight.",
        "date": "2024-01-15"
    }
]

class ReviewCreate(BaseModel):
    hotel_name: str
    city: str
    rating: int
    review_text: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the Hotel Review Visualization and Analysis Dashboard API"}

@app.get("/api/reviews")
def get_reviews(
    hotel_name: Optional[str] = None,
    sentiment: Optional[str] = None,
    min_rating: Optional[int] = Query(None, ge=1, le=5)
):
    filtered = REVIEWS_DB
    if hotel_name:
        filtered = [r for r in filtered if hotel_name.lower() in r["hotel_name"].lower()]
    if sentiment:
        filtered = [r for r in filtered if r["sentiment"].lower() == sentiment.lower()]
    if min_rating is not None:
        filtered = [r for r in filtered if r["rating"] >= min_rating]
    return filtered

@app.post("/api/reviews", status_code=201)
def create_review(review: ReviewCreate):
    # Simple rule-based sentiment analysis
    if review.rating >= 4:
        sentiment = "Positive"
    elif review.rating == 3:
        sentiment = "Neutral"
    else:
        sentiment = "Negative"
    
    new_id = max([r["id"] for r in REVIEWS_DB]) + 1 if REVIEWS_DB else 1
    new_entry = {
        "id": new_id,
        "hotel_name": review.hotel_name,
        "city": review.city,
        "rating": review.rating,
        "sentiment": sentiment,
        "review_text": review.review_text,
        "date": "2024-03-01"
    }
    REVIEWS_DB.append(new_entry)
    return new_entry

@app.get("/api/analytics")
def get_analytics():
    total_reviews = len(REVIEWS_DB)
    if total_reviews == 0:
        return {"total_reviews": 0, "avg_rating": 0, "sentiment_breakdown": {}, "hotel_ratings": {}}
    
    avg_rating = sum(r["rating"] for r in REVIEWS_DB) / total_reviews
    
    sentiment_breakdown = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for r in REVIEWS_DB:
        sentiment_breakdown[r["sentiment"]] = sentiment_breakdown.get(r["sentiment"], 0) + 1
        
    hotel_stats = {}
    for r in REVIEWS_DB:
        h = r["hotel_name"]
        if h not in hotel_stats:
            hotel_stats[h] = {"total_score": 0, "count": 0}
        hotel_stats[h]["total_score"] += r["rating"]
        hotel_stats[h]["count"] += 1
        
    hotel_ratings = {h: round(stats["total_score"] / stats["count"], 2) for h, stats in hotel_stats.items()}
    
    return {
        "total_reviews": total_reviews,
        "avg_rating": round(avg_rating, 2),
        "sentiment_breakdown": sentiment_breakdown,
        "hotel_ratings": hotel_ratings
    }
