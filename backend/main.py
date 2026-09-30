from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

class Review(BaseModel):
    hotel_name: str
    author: str
    rating: int
    comment: str
    date: str

# In-memory storage for reviews with a default sample review
reviews_db = [
    {
        "hotel_name": "Grand Hotel",
        "author": "Alice Smith",
        "rating": 4,
        "comment": "Great location and friendly staff.",
        "date": "2023-10-01"
    }
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[Review])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED, response_model=Review)
def create_review(review: Review):
    review_data = review.dict()
    reviews_db.append(review_data)
    return review_data

@app.get("/api/analytics")
def get_analytics():
    total_reviews = len(reviews_db)
    average_rating = sum(r["rating"] for r in reviews_db) / total_reviews if total_reviews > 0 else 0
    return {
        "total_reviews": total_reviews,
        "average_rating": average_rating
    }
