from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

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
    rating: int = Field(..., ge=1, le=5)
    sentiment: str
    comment: str
    date: str

class ReviewCreate(BaseModel):
    hotel_name: str
    reviewer_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    date: str

# In-memory database with initial sample data
reviews_db: List[Review] = [
    Review(
        id=1,
        hotel_name="Grand Palace Hotel",
        reviewer_name="Alice Smith",
        rating=5,
        sentiment="Positive",
        comment="Exceptional service and wonderful ocean view! Will definitely come back.",
        date="2023-10-15"
    ),
    Review(
        id=2,
        hotel_name="Grand Palace Hotel",
        reviewer_name="Bob Jones",
        rating=2,
        sentiment="Negative",
        comment="Room was noisy and the air conditioning broke down during the night.",
        date="2023-10-18"
    ),
    Review(
        id=3,
        hotel_name="City Express Inn",
        reviewer_name="Charlie Brown",
        rating=4,
        sentiment="Positive",
        comment="Clean rooms and very close to the central station. Great value.",
        date="2023-10-20"
    ),
    Review(
        id=4,
        hotel_name="Seaside Resort",
        reviewer_name="Diana Prince",
        rating=3,
        sentiment="Neutral",
        comment="Average experience. Food at the restaurant was mediocre, but the pool is nice.",
        date="2023-10-22"
    ),
    Review(
        id=5,
        hotel_name="City Express Inn",
        reviewer_name="Evan Wright",
        rating=1,
        sentiment="Negative",
        comment="Terrible customer service at reception. Unfriendly staff.",
        date="2023-10-25"
    )
]

def compute_sentiment(rating: int, comment: str) -> str:
    # Simple rule-based sentiment analysis for demonstration
    if rating >= 4:
        return "Positive"
    elif rating <= 2:
        return "Negative"
    else:
        text = comment.lower()
        if any(w in text for w in ["great", "excellent", "wonderful", "love", "amazing"]):
            return "Positive"
        elif any(w in text for w in ["terrible", "bad", "poor", "worst", "awful"]):
            return "Negative"
        return "Neutral"

@app.get("/api/reviews", response_model=List[Review])
def get_reviews(
    hotel: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None),
    rating: Optional[int] = Query(None)
):
    filtered = reviews_db
    if hotel:
        filtered = [r for r in filtered if hotel.lower() in r.hotel_name.lower()]
    if sentiment:
        filtered = [r for r in filtered if r.sentiment.lower() == sentiment.lower()]
    if rating:
        filtered = [r for r in filtered if r.rating == rating]
    return filtered

@app.post("/api/reviews", response_model=Review, status_code=201)
def create_review(payload: ReviewCreate):
    new_id = max([r.id for r in reviews_db], default=0) + 1
    sentiment = compute_sentiment(payload.rating, payload.comment)
    new_review = Review(
        id=new_id,
        hotel_name=payload.hotel_name,
        reviewer_name=payload.reviewer_name,
        rating=payload.rating,
        sentiment=sentiment,
        comment=payload.comment,
        date=payload.date
    )
    reviews_db.append(new_review)
    return new_review

@app.get("/api/analytics")
def get_analytics():
    total_reviews = len(reviews_db)
    if total_reviews == 0:
        return {
            "total_reviews": 0,
            "average_rating": 0.0,
            "sentiment_breakdown": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "hotel_breakdown": {}
        }
    
    avg_rating = sum(r.rating for r in reviews_db) / total_reviews
    
    sentiments = {"Positive": 0, "Neutral": 0, "Negative": 0}
    hotels = {}
    
    for r in reviews_db:
        if r.sentiment in sentiments:
            sentiments[r.sentiment] += 1
        else:
            sentiments[r.sentiment] = 1
            
        if r.hotel_name not in hotels:
            hotels[r.hotel_name] = {"count": 0, "total_rating": 0}
        hotels[r.hotel_name]["count"] += 1
        hotels[r.hotel_name]["total_rating"] += r.rating
        
    hotel_breakdown = {
        h: round(data["total_rating"] / data["count"], 2) 
        for h, data in hotels.items()
    }

    return {
        "total_reviews": total_reviews,
        "average_rating": round(avg_rating, 2),
        "sentiment_breakdown": sentiments,
        "hotel_breakdown": hotel_breakdown
    }
