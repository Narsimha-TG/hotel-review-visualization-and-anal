from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, List
import os

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Payload schema
class ReviewCreate(BaseModel):
    hotel_name: str
    author: Optional[str] = "Anonymous"
    reviewer_name: Optional[str] = None
    rating: int = Field(..., ge=1, le=5)
    comment: str
    date: Optional[str] = None

# Initial mock data
MOCK_REVIEWS = [
    {"id": 1, "hotel_name": "Grand Plaza", "author": "Alice Smith", "rating": 5, "comment": "Exceptional service!", "sentiment": "Positive", "date": "2023-11-01"},
    {"id": 2, "hotel_name": "Ocean Breeze", "author": "Bob Jones", "rating": 2, "comment": "Room was dirty.", "sentiment": "Negative", "date": "2023-11-02"},
    {"id": 3, "hotel_name": "Mountain View", "author": "Charlie Brown", "rating": 4, "comment": "Great location.", "sentiment": "Neutral", "date": "2023-11-03"}
]

# 1. Health check route
@app.get("/api/health")
def health_check():
    return {"status": "healthy"}

# 2. Review creation route returning 201 status code
@app.post("/api/reviews", status_code=status.HTTP_201_CREATED)
def create_review(payload: ReviewCreate):
    new_id = len(MOCK_REVIEWS) + 1
    review_dict = payload.model_dump() if hasattr(payload, "model_dump") else payload.dict()
    review_dict["id"] = new_id
    if not review_dict.get("author") and review_dict.get("reviewer_name"):
        review_dict["author"] = review_dict["reviewer_name"]
    review_dict["sentiment"] = "Positive" if review_dict["rating"] >= 4 else ("Negative" if review_dict["rating"] <= 2 else "Neutral")
    MOCK_REVIEWS.append(review_dict)
    return review_dict

# 3. Reviews list route
@app.get("/api/reviews")
def get_reviews():
    return MOCK_REVIEWS

# 4. Analytics & Dashboard route
@app.get("/api/analytics")
@app.get("/api/dashboard")
def get_analytics():
    total = len(MOCK_REVIEWS)
    avg_rating = sum(r["rating"] for r in MOCK_REVIEWS) / total if total > 0 else 0
    return {
        "total_reviews": total,
        "average_rating": round(avg_rating, 2),
        "ratings_breakdown": {
            f"{i} Stars": sum(1 for r in MOCK_REVIEWS if r["rating"] == i) for i in range(1, 6)
        }
    }

# 5. Frontend index
@app.get("/")
def serve_index():
    index_path = os.path.join("frontend", "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return HTMLResponse("<h1>Frontend index.html not found</h1>", status_code=404)