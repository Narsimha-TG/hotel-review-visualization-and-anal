from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Review(BaseModel):
    id: int = None
    hotel_name: str
    review_text: str
    rating: float

# In-memory storage for demonstration/tests
reviews_db = [
    {"id": 1, "hotel_name": "Hotel A", "review_text": "Great stay!", "rating": 5.0},
    {"id": 2, "hotel_name": "Hotel B", "review_text": "Average experience.", "rating": 3.0},
    {"id": 3, "hotel_name": "Hotel C", "review_text": "Good service.", "rating": 4.0}
]

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews", response_model=List[Review])
def get_reviews():
    return reviews_db

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED, response_model=Review)
def create_review(review: Review):
    new_id = len(reviews_db) + 1
    new_review = review.dict()
    new_review["id"] = new_id
    reviews_db.append(new_review)
    return new_review

@app.get("/api/analytics")
def get_analytics():
    total = len(reviews_db)
    avg = sum(r["rating"] for r in reviews_db) / total if total > 0 else 0.0
    return {
        "total_reviews": total,
        "avg_rating": avg,
        "average_rating": avg
    }
