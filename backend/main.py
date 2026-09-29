from fastapi import FastAPI, status
from pydantic import BaseModel

app = FastAPI()

class Review(BaseModel):
    hotel_name: str
    review_text: str
    rating: float

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews")
def get_reviews():
    return [
        {"hotel_name": "Grand Hotel", "review_text": "Amazing stay!", "rating": 5.0},
        {"hotel_name": "City Inn", "review_text": "Average experience.", "rating": 3.0}
    ]

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED)
def create_review(review: Review):
    return {"message": "Review created successfully", "review": review}

@app.get("/api/analytics")
def get_analytics():
    return {
        "total_reviews": 150,
        "average_rating": 4.2,
        "sentiment_breakdown": {
            "positive": 100,
            "neutral": 30,
            "negative": 20
        }
    }
