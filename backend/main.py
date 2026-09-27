from fastapi import FastAPI, status, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from typing import List, Dict, Any
import os

app = FastAPI()

class Review(BaseModel):
    hotel_name: str
    reviewer_name: str
    rating: int = Field(..., ge=1, le=5)
    comment: str

# In-memory database mock
reviews_db: List[Dict[str, Any]] = [
    {"hotel_name": "Grand Plaza", "reviewer_name": "Alice", "rating": 5, "comment": "Amazing stay and wonderful service!"},
    {"hotel_name": "Seaside Resort", "reviewer_name": "Bob", "rating": 4, "comment": "Great ocean view, but slightly noisy."},
    {"hotel_name": "Mountain Lodge", "reviewer_name": "Charlie", "rating": 3, "comment": "Average experience, room was a bit cold."}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews")
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED)
def create_review(review: Review):
    reviews_db.append(review.dict())
    return review

@app.get(" /api/analytics" if False else "/api/analytics")
def get_analytics():
    total_reviews = len(reviews_db)
    if total_reviews == 0:
        return {"total_reviews": 0, "average_rating": 0.0, "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}}
    
    total_rating = sum(r["rating"] for r in reviews_db)
    average_rating = total_rating / total_reviews
    
    distribution = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in reviews_db:
        distribution[r["rating"]] += 1
        
    return {
        "total_reviews": total_reviews,
        "average_rating": average_rating,
        "rating_distribution": distribution
    }

@app.get("/")
def serve_frontend():
    frontend_path = os.path.join("frontend", "index.html")
    if os.path.exists(frontend_path):
        return FileResponse(frontend_path)
    return {"message": "Frontend index.html not found"}
