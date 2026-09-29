from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class Review(BaseModel):
    hotel_name: str
    author: str
    rating: int = Field(..., ge=1, le=5)
    comment: str
    date: str

reviews_db = [
    {
        "id": 1,
        "hotel_name": "Luxury Inn",
        "author": "Alice Smith",
        "rating": 4,
        "comment": "Great stay, very clean.",
        "date": "2023-10-01"
    },
    {
        "id": 2,
        "hotel_name": "Budget Stay",
        "author": "Bob Jones",
        "rating": 2,
        "comment": "Not very clean, noisy.",
        "date": "2023-10-05"
    }
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[dict])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED)
def create_review(review: Review):
    new_review = review.dict()
    new_review["id"] = len(reviews_db) + 1
    reviews_db.append(new_review)
    return new_review

@app.get("/api/analytics")
def get_analytics():
    total_reviews = len(reviews_db)
    avg_rating = sum(r["rating"] for r in reviews_db) / total_reviews if total_reviews > 0 else 0
    return {
        "total_reviews": total_reviews,
        "average_rating": avg_rating
}
