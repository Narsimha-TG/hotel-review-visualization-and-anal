from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import uuid
import json
import re

app = FastAPI(
    title="Hotel Review Visualization and Analysis Dashboard",
    description="Backend API for hotel reviews, sentiment analysis, and interactive visualizations.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory database with initial rich dataset
INITIAL_REVIEWS = [
    {
        "id": "rev-101",
        "hotel_name": "Grand Plaza Resort",
        "reviewer_name": "Alice Johnson",
        "rating": 5,
        "review_text": "Absolute perfection! The staff were exceptionally welcoming, the rooms were spotless, and the ocean view was breathtaking. Breakfast buffet had endless options.",
        "sentiment": "Positive"
    },
    {
        "id": "rev-102",
        "hotel_name": "Grand Plaza Resort",
        "reviewer_name": "Bob Smith",
        "rating": 2,
        "review_text": "Disappointing stay. The room smelled musty, and air conditioning broke down on the second night. Maintenance took hours to respond.",
        "sentiment": "Negative"
    },
    {
        "id": "rev-103",
        "hotel_name": "Urban Boutique Hotel",
        "reviewer_name": "Claire Davis",
        "rating": 4,
        "review_text": "Great downtown location, walking distance to all major attractions. Clean rooms and friendly front desk. A bit noisy at night from street traffic.",
        "sentiment": "Positive"
    },
    {
        "id": "rev-104",
        "hotel_name": "Urban Boutique Hotel",
        "reviewer_name": "David Lee",
        "rating": 3,
        "review_text": "Average experience. Room was smaller than expected and Wi-Fi was unstable. Location is the only real highlight.",
        "sentiment": "Neutral"
    },
    {
        "id": "rev-105",
        "hotel_name": "Seaside Paradise Spa",
        "reviewer_name": "Elena Rostova",
        "rating": 5,
        "review_text": "The spa treatments were world-class and the pool area is pristine. Exceptional service from start to finish. Highly recommend!",
        "sentiment": "Positive"
    },
    {
        "id": "rev-106",
        "hotel_name": "Mountain Lodge Retreat",
        "reviewer_name": "Frank Miller",
        "rating": 4,
        "review_text": "Cozy cabin with a stunning fireplace view. Perfect weekend getaway. Food at the lodge restaurant was delicious.",
        "sentiment": "Positive"
    },
    {
        "id": "rev-107",
        "hotel_name": "Mountain Lodge Retreat",
        "reviewer_name": "Grace Hopper",
        "rating": 1,
        "review_text": "Terrible service and freezing room. The heating system didn't work and management refused to offer another room. Will never return.",
        "sentiment": "Negative"
    },
    {
        "id": "rev-108",
        "hotel_name": "Grand Plaza Resort",
        "reviewer_name": "Hannah Abbott",
        "rating": 4,
        "review_text": "Loved the pool and beach access. Food was good although slightly overpriced. Cleanliness was top notch.",
        "sentiment": "Positive"
    },
    {
        "id": "rev-109",
        "hotel_name": "Urban Boutique Hotel",
        "reviewer_name": "Ian Malcolm",
        "rating": 2,
        "review_text": "Bed was uncomfortable and bathroom plumbing made loud noises all night. Staff were indifferent.",
        "sentiment": "Negative"
    },
    {
        "id": "rev-110",
        "hotel_name": "Seaside Paradise Spa",
        "reviewer_name": "Julia Roberts",
        "rating": 3,
        "review_text": "Nice location and decent amenities, but check-in took over 45 minutes which was frustrating after a long flight.",
        "sentiment": "Neutral"
    }
]

reviews_db = INITIAL_REVIEWS.copy()

class ReviewCreate(BaseModel):
    hotel_name: str
    reviewer_name: str
    rating: int = Field(..., ge=1, le=5)
    review_text: str

class ReviewResponse(BaseModel):
    id: str
    hotel_name: str
    reviewer_name: str
    rating: int
    review_text: str
    sentiment: str

def analyze_sentiment(text: str, rating: int) -> str:
    text_lower = text.lower()
    positive_words = ['great', 'excellent', 'amazing', 'perfect', 'wonderful', 'breathtaking', 'friendly', 'clean', 'love', 'loved', 'delicious', 'pristine', 'top', 'recommend']
    negative_words = ['terrible', 'disappointing', 'musty', 'broken', 'noisy', 'poor', 'uncomfortable', 'frustrating', 'refused', 'never', 'bad', 'horrible']
    
    pos_count = sum(1 for w in positive_words if w in text_lower)
    neg_count = sum(1 for w in negative_words if w in text_lower)
    
    if rating >= 4 and neg_count == 0:
        return "Positive"
    if rating <= 2 and pos_count == 0:
        return "Negative"
    if pos_count > neg_count:
        return "Positive"
    elif neg_count > pos_count:
        return "Negative"
    else:
        return "Neutral" if rating == 3 else ("Positive" if rating > 3 else "Negative")

@app.get("/api/hotels")
def get_hotels():
    hotels = sorted(list(set(r["hotel_name"] for r in reviews_db)))
    return {"hotels": hotels}

@app.get("/api/reviews")
def get_reviews(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    hotel: Optional[str] = None,
    sentiment: Optional[str] = None,
    search: Optional[str] = None
):
    filtered = reviews_db
    if hotel:
        filtered = [r for r in filtered if r["hotel_name"].lower() == hotel.lower()]
    if sentiment:
        filtered = [r for r in filtered if r["sentiment"].lower() == sentiment.lower()]
    if search:
        s = search.lower()
        filtered = [r for r in filtered if s in r["review_text"].lower() or s in r["hotel_name"].lower() or s in r["reviewer_name"].lower()]

    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    paginated = filtered[start:end]

    return {
        "reviews": paginated,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": (total + limit - 1) // limit if limit > 0 else 1
        }
    }

@app.post("/api/reviews", status_code=201)
def create_review(payload: ReviewCreate):
    review_id = f"rev-{uuid.uuid4().hex[:6]}"
    sentiment = analyze_sentiment(payload.review_text, payload.rating)
    new_review = {
        "id": review_id,
        "hotel_name": payload.hotel_name,
        "reviewer_name": payload.reviewer_name,
        "rating": payload.rating,
        "review_text": payload.review_text,
        "sentiment": sentiment
    }
    reviews_db.insert(0, new_review)
    return new_review

@app.delete("/api/reviews/{review_id}")
def delete_review(review_id: str):
    global reviews_db
    initial_len = len(reviews_db)
    reviews_db = [r for r in reviews_db if r["id"] != review_id]
    if len(reviews_db) == initial_len:
        raise HTTPException(status_code=404, detail="Review not found")
    return {"message": "Review deleted successfully"}

@app.get("/api/analytics/stats")
def get_analytics_stats(hotel: Optional[str] = None):
    filtered = reviews_db
    if hotel:
        filtered = [r for r in filtered if r["hotel_name"].lower() == hotel.lower()]

    total_reviews = len(filtered)
    if total_reviews == 0:
        return {
            "total_reviews": 0,
            "average_rating": 0.0,
            "positive_percentage": 0.0,
            "unique_hotels": len(set(r["hotel_name"] for r in reviews_db)),
            "sentiment_breakdown": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "top_hotels": []
        }

    avg_rating = sum(r["rating"] for r in filtered) / total_reviews
    
    sentiment_counts = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for r in filtered:
        sentiment_counts[r["sentiment"]] = sentiment_counts.get(r["sentiment"], 0) + 1

    positive_percentage = (sentiment_counts["Positive"] / total_reviews) * 100

    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in filtered:
        rating_dist[r["rating"]] = rating_dist.get(r["rating"], 0) + 1

    # Top hotels rating calculation
    hotel_map = {}
    for r in reviews_db:
        h = r["hotel_name"]
        if h not in hotel_map:
            hotel_map[h] = []
        hotel_map[h].append(r["rating"])

    top_hotels = []
    for h, ratings in hotel_map.items():
        top_hotels.append({
            "hotel": h,
            "avg_rating": round(sum(ratings) / len(ratings), 2),
            "count": len(ratings)
        })
    top_hotels = sorted(top_hotels, key=lambda x: x["avg_rating"], reverse=True)[:5]

    return {
        "total_reviews": total_reviews,
        "average_rating": round(avg_rating, 2),
        "positive_percentage": round(positive_percentage, 1),
        "unique_hotels": len(set(r["hotel_name"] for r in reviews_db)),
        "sentiment_breakdown": sentiment_counts,
        "rating_distribution": rating_dist,
        "top_hotels": top_hotels
    }

@app.get("/api/analytics/nlp")
def get_nlp_analytics(hotel: Optional[str] = None):
    filtered = reviews_db
    if hotel:
        filtered = [r for r in filtered if r["hotel_name"].lower() == hotel.lower()]

    aspects = {
        "Staff & Service": {"Positive": 0, "Neutral": 0, "Negative": 0},
        "Cleanliness": {"Positive": 0, "Neutral": 0, "Negative": 0},
        "Location": {"Positive": 0, "Neutral": 0, "Negative": 0},
        "Rooms & Comfort": {"Positive": 0, "Neutral": 0, "Negative": 0},
        "Food & Dining": {"Positive": 0, "Neutral": 0, "Negative": 0}
    }

    aspect_keywords = {
        "Staff & Service": ["staff", "service", "front desk", "management", "reception"],
        "Cleanliness": ["clean", "spotless", "smelled", "musty", "hygiene"],
        "Location": ["location", "downtown", "beach", "view", "walking distance"],
        "Rooms & Comfort": ["room", "bed", "ac", "air conditioning", "heating", "cabin"],
        "Food & Dining": ["breakfast", "food", "restaurant", "buffet", "dining"]
    }

    for r in filtered:
        text = r["review_text"].lower()
        sent = r["sentiment"]
        for aspect, keywords in aspect_keywords.items():
            if any(kw in text for kw in keywords):
                aspects[aspect][sent] += 1

    # Extract top keywords
    word_counts = {}
    stop_words = set(["the", "and", "a", "to", "of", "in", "is", "it", "was", "for", "on", "with", "as", "at", "by", "an", "be", "this", "my", "but", "from", "that", "are", "were", "not", "hotel", "stay"])
    
    for r in filtered:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', r["review_text"].lower())
        for w in words:
            if w not in stop_words:
                word_counts[w] = word_counts.get(w, 0) + 1

    top_keywords = [{"word": k, "count": v} for k, v in sorted(word_counts.items(), key=lambda item: item[1], reverse=True)[:8]]

    return {
        "aspect_sentiments": aspects,
        "top_keywords": top_keywords
    }

@app.get("/")
def serve_frontend():
    frontend_path = os.path.join(os.path.dirname(__file__), "../frontend/index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return HTMLResponse("<h1>Hotel Review Visualization Dashboard API is running. Frontend index.html not found.</h1>")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
