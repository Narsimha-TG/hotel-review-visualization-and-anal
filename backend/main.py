from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(
    title="Hotel Review Visualization and Analysis Dashboard",
    description="Backend API for hotel reviews sentiment and rating analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mock dataset for Hotel Reviews
MOCK_REVIEWS = [
    {
        "id": 1,
        "author": "Sarah Jenkins",
        "rating": 5,
        "sentiment": "positive",
        "text": "Absolute gem of a hotel! The staff went above and beyond to make our anniversary special. Sparkling clean rooms and fantastic breakfast.",
        "date": "2025-02-18"
    },
    {
        "id": 2,
        "author": "Michael Chang",
        "rating": 2,
        "sentiment": "negative",
        "text": "Very disappointing stay. The AC unit was extremely loud all night and the front desk staff was indifferent to our complaints.",
        "date": "2025-02-17"
    },
    {
        "id": 3,
        "author": "Elena Rostova",
        "rating": 4,
        "sentiment": "positive",
        "text": "Great location right in the city center. Walkable to all major attractions. Room was slightly small but very cozy.",
        "date": "2025-02-15"
    },
    {
        "id": 4,
        "author": "David Smith",
        "rating": 3,
        "sentiment": "neutral",
        "text": "Average experience overall. The pool was closed for maintenance which was a bummer, but the restaurant had good food.",
        "date": "2025-02-14"
    },
    {
        "id": 5,
        "author": "Jessica Taylor",
        "rating": 5,
        "sentiment": "positive",
        "text": "Breathtaking ocean views and world-class spa facilities. Can't wait to come back for our next vacation!",
        "date": "2025-02-12"
    },
    {
        "id": 6,
        "author": "Robert Downey",
        "rating": 1,
        "sentiment": "negative",
        "text": "Terrible customer service and found hair in the bathroom upon arrival. Will not be recommending to anyone.",
        "date": "2025-02-10"
    },
    {
        "id": 7,
        "author": "Amanda White",
        "rating": 4,
        "sentiment": "positive",
        "text": "Very comfortable beds and quiet rooms. Excellent choice for business travelers looking for reliable Wi-Fi and workspace.",
        "date": "2025-02-09"
    },
    {
        "id": 8,
        "author": "Carlos Santana",
        "rating": 3,
        "sentiment": "neutral",
        "text": "Decent hotel for the price point. Breakfast buffet could use more variety, but room cleanliness was satisfactory.",
        "date": "2025-02-08"
    },
    {
        "id": 9,
        "author": "Emily Blunt",
        "rating": 5,
        "sentiment": "positive",
        "text": "Immaculate design, friendly concierge, and delicious cocktails at the rooftop bar. 10/10 stay!",
        "date": "2025-02-05"
    },
    {
        "id": 10,
        "author": "Liam Neeson",
        "rating": 2,
        "sentiment": "negative",
        "text": "Room was much smaller than pictured online and hallway noise kept waking us up.",
        "date": "2025-02-03"
    }
]

class Review(BaseModel):
    id: int
    author: str
    rating: int
    sentiment: str
    text: str
    date: str

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "Hotel Review Dashboard API is running"}

@app.get("/api/reviews")
def get_reviews(sentiment: Optional[str] = Query(None, description="Filter by sentiment: positive, neutral, negative")):
    filtered = MOCK_REVIEWS
    if sentiment and sentiment.lower() != "all":
        filtered = [r for r in MOCK_REVIEWS if r["sentiment"] == sentiment.lower()]

    # Calculate statistics
    total_reviews = len(MOCK_REVIEWS)
    average_rating = sum(r["rating"] for r in MOCK_REVIEWS) / total_reviews if total_reviews > 0 else 0
    
    sentiment_counts = {"positive": 0, "neutral": 0, "negative": 0}
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}

    for r in MOCK_REVIEWS:
        s = r["sentiment"]
        if s in sentiment_counts:
            sentiment_counts[s] += 1
        rt = r["rating"]
        if rt in rating_counts:
            rating_counts[rt] += 1

    stats = {
        "total_reviews": total_reviews,
        "average_rating": round(average_rating, 2),
        "sentiment_counts": sentiment_counts,
        "rating_counts": rating_counts
    }

    return {
        "stats": stats,
        "reviews": filtered
    }

# Serve frontend index.html at root if frontend file exists
@app.get("/")
def serve_index():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "Welcome to Hotel Review Analysis API. Frontend index.html not found in container root."}
