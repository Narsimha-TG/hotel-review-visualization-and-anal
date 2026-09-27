from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os

app = FastAPI(
    title="Hotel Review Visualization and Analysis Dashboard API",
    version="1.0.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Review(BaseModel):
    id: int
    hotel_name: str
    reviewer_name: str
    rating: int
    sentiment: str
    review_text: str

# Mock dataset for hotel reviews
INITIAL_REVIEWS = [
    Review(id=1, hotel_name="Grand Palace Hotel", reviewer_name="Alice Smith", rating=5, sentiment="Positive", review_text="Absolute masterpiece of a hotel! Exceptional service, immaculate rooms, and great dining options."),
    Review(id=2, hotel_name="Grand Palace Hotel", reviewer_name="Bob Jones", rating=2, sentiment="Negative", review_text="Disappointing stay. The room smelled damp and the front desk staff was quite rude upon check-in."),
    Review(id=3, hotel_name="Seaside Resort & Spa", reviewer_name="Charlie Brown", rating=4, sentiment="Positive", review_text="Wonderful ocean view and relaxing spa treatments. Will definitely come back for another vacation."),
    Review(id=4, hotel_name="Seaside Resort & Spa", reviewer_name="Diana Prince", rating=3, sentiment="Neutral", review_text="The location is fantastic right by the beach, but the breakfast buffet was mediocre and overpriced."),
    Review(id=5, hotel_name="Urban Boutique Inn", reviewer_name="Ethan Hunt", rating=5, sentiment="Positive", review_text="Super stylish decor, lightning-fast Wi-Fi, and right in the heart of downtown. Perfect for business travelers."),
    Review(id=6, hotel_name="Urban Boutique Inn", reviewer_name="Fiona Glenanne", rating=1, sentiment="Negative", review_text="Extremely noisy at night due to street traffic and thin walls. Slept very poorly."),
    Review(id=7, hotel_name="Mountain View Lodge", reviewer_name="George Clark", rating=4, sentiment="Positive", review_text="Cozy cabin vibe with breathtaking mountain vistas. The fireplace in the lobby was a huge plus."),
    Review(id=8, hotel_name="Mountain View Lodge", reviewer_name="Hannah Abbott", rating=3, sentiment="Neutral", review_text="Nice scenery, but the heating in our room was inconsistent. Staff was polite when we reported it."),
    Review(id=9, hotel_name="Grand Palace Hotel", reviewer_name="Ian Malcolm", rating=4, sentiment="Positive", review_text="Extremely luxurious amenities and top-tier security. Truly felt pampered throughout."),
    Review(id=10, hotel_name="Seaside Resort & Spa", reviewer_name="Julia Roberts", rating=5, sentiment="Positive", review_text="Paradise found! Pristine pools, attentive pool-side service, and breathtaking sunset views.")
]

@app.get("/api/reviews")
def get_reviews():
    return {
        "total": len(INITIAL_REVIEWS),
        "reviews": [r.dict() for r in INITIAL_REVIEWS]
    }

@app.post("/api/reviews", status_code=201)
def add_review(review: Review):
    INITIAL_REVIEWS.append(review)
    return {"message": "Review added successfully", "review": review.dict()}

# Mount static files / frontend
if os.path.exists("frontend"):
    app.mount("/static", StaticFiles(directory="frontend"), name="static")

    @app.get("/")
    def serve_index():
        return FileResponse(os.path.join("frontend", "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
