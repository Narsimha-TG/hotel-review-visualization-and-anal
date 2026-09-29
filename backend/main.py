from fastapi import FastAPI, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Review(BaseModel):
    id: Optional[int] = None
    hotel_name: str
    rating: int
    comment: str

# In-memory storage for reviews
reviews_db = [
    {"id": 1, "hotel_name": "Grand Hotel", "rating": 5, "comment": "Excellent stay!"},
    {"id": 2, "hotel_name": "Beach Resort", "rating": 3, "comment": "Average experience."}
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
    review_dict = review.dict()
    review_dict["id"] = new_id
    reviews_db.append(review_dict)
    return review_dict

@app.get("/api/analytics")
def get_analytics():
    total_reviews = len(reviews_db)
    avg_rating = sum(r["rating"] for r in reviews_db) / total_reviews if total_reviews > 0 else 0
    return {
        "total_reviews": total_reviews,
        "average_rating": avg_rating
}
