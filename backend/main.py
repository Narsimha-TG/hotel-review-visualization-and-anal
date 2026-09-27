from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

@app.get("/api/reviews")
def get_reviews():
    return [
        {
            "id": 1,
            "hotel_name": "Grand Plaza",
            "review_text": "Wonderful stay, excellent service and clean rooms!",
            "rating": 5,
            "sentiment": "Positive"
        },
        {
            "id": 2,
            "hotel_name": "City Inn",
            "review_text": "Average experience, noisy hallway at night.",
            "rating": 3,
            "sentiment": "Neutral"
        }
    ]

@app.get("/api/analytics")
def get_analytics():
    return {
        "total_reviews": 2,
        "average_rating": 4.0,
        "sentiment_breakdown": {
            "Positive": 1,
            "Neutral": 1,
            "Negative": 0
        }
    }
