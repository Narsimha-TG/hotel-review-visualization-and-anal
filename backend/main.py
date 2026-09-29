from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Review(BaseModel):
    hotel_name: str
    author: str
    rating: int
    comment: str
    date: str

# In-memory database for reviews
reviews_db = []

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[Review])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED, response_model=Review)
def create_review(review: Review):
    reviews_db.append(review.dict())
    return review

@app.get("/api/analytics")
def get_analytics():
    total_reviews = len(reviews_db)
    if total_reviews > 0:
        avg_rating = sum(r["rating"] for r in reviews_db) / total_reviews
    else:
        avg_rating = 0.0
    
    return {
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
        "average_rating": avg_rating
    }
