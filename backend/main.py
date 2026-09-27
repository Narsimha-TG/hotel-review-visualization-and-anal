from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import statistics

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    hotel_name: str
    reviewer_name: str
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: str
    sentiment: str

class ReviewCreate(BaseModel):
    hotel_name: str
    reviewer_name: str
    rating: float = Field(..., ge=1.0, le=5.0)
    comment: str

# In-memory database with sample seed data
reviews_db: List[Review] = [
    Review(id=1, hotel_name="Grand Palace", reviewer_name="Alice Smith", rating=4.5, comment="Exceptional service and wonderful views from the suite.", sentiment="Positive"),
    Review(id=2, hotel_name="Grand Palace", reviewer_name="Bob Jones", rating=2.0, comment="Noisy hallways and the air conditioning was broken all night.", sentiment="Negative"),
    Review(id=3, hotel_name="Ocean Breeze", reviewer_name="Charlie Brown", rating=5.0, comment="Direct beach access, pristine rooms, and delicious breakfast.", sentiment="Positive"),
    Review(id=4, hotel_name="Ocean Breeze", reviewer_name="Diana Prince", rating=3.5, comment="Decent stay overall, but the Wi-Fi connection was very spotty.", sentiment="Neutral"),
    Review(id=5, hotel_name="Mountain Retreat", reviewer_name="Evan Wright", rating=1.5, comment="Extremely outdated decor and terrible customer support.", sentiment="Negative")
]

def compute_sentiment(rating: float, comment: str) -> str:
    # Simple heuristic sentiment analysis for demonstration
    lower_comment = comment.lower()
    pos_words = ["great", "wonderful", "exceptional", "pristine", "delicious", "loved", "best", "amazing"]
    neg_words = ["noisy", "broken", "terrible", "outdated", "poor", "worst", "horrible", "bad"]
    
    pos_count = sum(1 for w in pos_words if w in lower_comment)
    neg_count = sum(1 for w in neg_words if w in lower_comment)
    
    if rating >= 4.0 or (pos_count > neg_count and rating >= 3.0):
        return "Positive"
    elif rating <= 2.5 or (neg_count > pos_count):
        return "Negative"
    else:
        return "Neutral"

@app.get("/api/health", tags=["System"])
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[Review], tags=["Reviews"])
def get_reviews(hotel: Optional[str] = None):
    if hotel:
        filtered = [r for r in reviews_db if r.hotel_name.lower() == hotel.lower()]
        return filtered
    return reviews_db

@app.post("/api/reviews", response_model=Review, status_code=201, tags=["Reviews"])
def create_review(payload: ReviewCreate):
    new_id = max([r.id for r in reviews_db], default=0) + 1
    sentiment = compute_sentiment(payload.rating, payload.comment)
    new_review = Review(
        id=new_id,
        hotel_name=payload.hotel_name,
        reviewer_name=payload.reviewer_name,
        rating=payload.rating,
        comment=payload.comment,
        sentiment=sentiment
    )
    reviews_db.append(new_review)
    return new_review

@app.get("/api/analytics", tags=["Analytics"])
def get_analytics():
    if not reviews_db:
        return {
            "total_reviews": 0,
            "average_rating": 0.0,
            "sentiment_breakdown": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "hotel_breakdown": {}
        }
    
    total_reviews = len(reviews_db)
    avg_rating = round(statistics.mean([r.rating for r in reviews_db]), 2)
    
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}
    for r in reviews_db:
        if r.sentiment in sentiments:
            sentiments[r.sentiment] += 1
            
    hotels = {}
    for r in reviews_db:
        if r.hotel_name not in hotels:
            hotels[r.hotel_name] = {"count": 0, "ratings": []}
        hotels[r.hotel_name]["count"] += 1
        hotels[r.hotel_name]["ratings"].append(r.rating)
        
    hotel_breakdown = {}
    for h, data in hotels.items():
        hotel_breakdown[h] = {
            "total_reviews": data["count"],
            "average_rating": round(statistics.mean(data["ratings"]), 2)
        }
        
    return {
        "total_reviews": total_reviews,
        "average_rating": avg_rating,
        "sentiment_breakdown": sentiments,
        "hotel_breakdown": hotel_breakdown
    }
