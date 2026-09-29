from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

class ReviewCreate(BaseModel):
    hotel_name: str
    author: str
    rating: int
    comment: str
    date: str

class Review(ReviewCreate):
    id: Optional[int] = None

reviews_db = []

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[Review])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED, response_model=Review)
def create_review(review: ReviewCreate):
    new_id = len(reviews_db) + 1
    review_data = review.model_dump()
    review_data["id"] = new_id
    reviews_db.append(review_data)
    return review_data

@app.get("/api/analytics")
def get_analytics():
    total_reviews = len(reviews_db)
    avg_rating = sum(r["rating"] for r in reviews_db) / total_reviews if total_reviews > 0 else 0.0
    return {
        "total_reviews": total_reviews,
        "average_rating": avg_rating
    }
