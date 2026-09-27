from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import os

app = FastAPI(title="Hotel Review Visualization and Analysis Dashboard")

# In-memory storage with default mock data
DEFAULT_DATA = [
    {"hotel_name": "Grand Plaza", "reviewer_name": "Alice Smith", "rating": 5, "sentiment": "Positive", "comment": "Amazing service and gorgeous rooms!"},
    {"hotel_name": "Grand Plaza", "reviewer_name": "Bob Jones", "rating": 4, "sentiment": "Positive", "comment": "Very clean, friendly staff."},
    {"hotel_name": "Seaside Resort", "reviewer_name": "Charlie Brown", "rating": 2, "sentiment": "Negative", "comment": "Noisy rooms and poor breakfast selection."},
    {"hotel_name": "Seaside Resort", "reviewer_name": "Diana Prince", "rating": 3, "sentiment": "Neutral", "comment": "Average stay, nothing special."},
    {"hotel_name": "Mountain Lodge", "reviewer_name": "Evan Wright", "rating": 5, "sentiment": "Positive", "comment": "Breathtaking views and cozy atmosphere."},
    {"hotel_name": "Urban Inn", "reviewer_name": "Fiona Gallagher", "rating": 1, "sentiment": "Negative", "comment": "Terrible hygiene and rude receptionist."}
];

df_reviews = pd.DataFrame(DEFAULT_DATA)

def compute_analytics(df: pd.DataFrame):
    if df.empty:
        return {
            "total_reviews": 0,
            "avg_rating": 0.0,
            "positive_percentage": 0.0,
            "negative_percentage": 0.0,
            "sentiment_counts": {},
            "rating_counts": {},
            "hotel_avg_ratings": {},
            "recent_reviews": []
        }

    total_reviews = len(df)
    avg_rating = float(df["rating"].mean()) if "rating" in df.columns else 0.0
    
    # Sentiment calculations
    sentiment_counts = df["sentiment"].value_counts().to_dict() if "sentiment" in df.columns else {}
    positive_count = sentiment_counts.get("Positive", 0)
    negative_count = sentiment_counts.get("Negative", 0)
    positive_percentage = (positive_count / total_reviews) * 100 if total_reviews > 0 else 0.0
    negative_percentage = (negative_count / total_reviews) * 100 if total_reviews > 0 else 0.0

    # Rating distribution
    rating_counts = df["rating"].value_counts().sort_index().to_dict() if "rating" in df.columns else {}
    # Convert keys to string for JSON consistency
    rating_counts = {str(k): v for k, v in rating_counts.items()}

    # Hotel avg ratings
    hotel_avg_ratings = {}
    if "hotel_name" in df.columns and "rating" in df.columns:
        hotel_avg_ratings = df.groupby("hotel_name")["rating"].mean().round(2).to_dict()

    # Recent reviews
    recent_reviews = df.tail(10).to_dict(orient="records")

    return {
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
        "positive_percentage": positive_percentage,
        "negative_percentage": negative_percentage,
        "sentiment_counts": sentiment_counts,
        "rating_counts": rating_counts,
        "hotel_avg_ratings": hotel_avg_ratings,
        "recent_reviews": recent_reviews
    }

@app.get("/")
def read_root():
    if os.path.exists("frontend/index.html"):
        with open("frontend/index.html", "r") as f:
            return HTMLResponse(content=f.read())
    return {"message": "Frontend index.html not found"}

@app.get("/api/analytics")
def get_analytics():
    global df_reviews
    return compute_analytics(df_reviews)

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    global df_reviews
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        # Normalize columns if needed
        expected_columns = ["hotel_name", "reviewer_name", "rating", "sentiment", "comment"]
        # Basic validation and fallback standardization
        df.columns = [c.strip().lower().replace(" ", "_") for c in df.columns]
        
        # Ensure mandatory columns exist
        if "rating" not in df.columns:
            raise HTTPException(status_code=400, detail="CSV must contain a 'rating' column")
        
        if "sentiment" not in df.columns:
            # Simple auto-sentiment generation if missing
            def guess_sentiment(r):
                try:
                    val = float(r)
                    if val >= 4: return "Positive"
                    elif val <= 2: return "Negative"
                    return "Neutral"
                except:
                    return "Neutral"
            df["sentiment"] = df["rating"].apply(guess_sentiment)
            
        if "hotel_name" not in df.columns:
            df["hotel_name"] = "Unknown Hotel"
            
        if "reviewer_name" not in df.columns:
            df["reviewer_name"] = "Anonymous"
            
        if "comment" not in df.columns:
            df["comment"] = ""

        df_reviews = df
        return compute_analytics(df_reviews)
    except Exception as e:

        raise HTTPException(status_code=400, detail=str(e))
