from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import pandas as pd
import io
import os

app = FastAPI()

# In-memory store for demo/default state
reviews_data = []

def compute_metrics(df):
    if df.empty:
        return {
            "total_reviews": 0,
            "avg_rating": 0.0,
            "sentiment_percentage": 0,
            "rating_counts": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0},
            "sentiment_counts": {"Positive": 0, "Neutral": 0, "Negative": 0},
            "reviews": []
        }

    # Normalize columns if needed
    # Expected columns: reviewer, rating, comment, sentiment
    if 'rating' not in df.columns:
        df['rating'] = 5
    if 'comment' not in df.columns:
        df['comment'] = ""
    if 'reviewer' not in df.columns:
        df['reviewer'] = "Anonymous"
    
    if 'sentiment' not in df.columns:
        def classify_sentiment(row):
            r = row['rating']
            if r >= 4:
                return 'Positive'
            elif r == 3:
                return 'Neutral'
            else:
                return 'Negative'
        df['sentiment'] = df.apply(classify_sentiment, axis=1)

    total_reviews = len(df)
    avg_rating = float(df['rating'].mean()) if total_reviews > 0 else 0.0

    rating_counts = df['rating'].value_counts().to_dict()
    # Ensure all ratings 1-5 exist
    for i in range(1, 6):
        if i not in rating_counts:
            rating_counts[i] = 0

    sentiment_counts = df['sentiment'].value_counts().to_dict()
    for s in ["Positive", "Neutral", "Negative"]:
        if s not in sentiment_counts:
            sentiment_counts[s] = 0

    positive_count = sentiment_counts.get("Positive", 0)
    sentiment_percentage = int((positive_count / total_reviews * 100)) if total_reviews > 0 else 0

    reviews = df.tail(50).to_dict(orient="records")

    return {
        "total_reviews": total_reviews,
        "avg_rating": avg_rating,
        "sentiment_percentage": sentiment_percentage,
        "rating_counts": rating_counts,
        "sentiment_counts": sentiment_counts,
        "reviews": reviews
    }

@app.get("/api/data")
async def get_data():
    global reviews_data
    if not reviews_data:
        # Return default dummy data if none uploaded
        df = pd.DataFrame([
            {"reviewer": "Alice Smith", "rating": 5, "comment": "Wonderful stay, exceptional staff!", "sentiment": "Positive"},
            {"reviewer": "Bob Jones", "rating": 2, "comment": "Room was noisy and outdated.", "sentiment": "Negative"},
            {"reviewer": "Charlie Brown", "rating": 3, "comment": "Average experience overall.", "sentiment": "Neutral"},
            {"reviewer": "Diana Prince", "rating": 4, "comment": "Great location and clean rooms.", "sentiment": "Positive"}
        ])
        return compute_metrics(df)
    
    df = pd.DataFrame(reviews_data)
    return compute_metrics(df)

@app.post("/api/upload")
async def upload_csv(file: UploadFile = File(...)):
    global reviews_data
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Invalid file format. Please upload a CSV file.")
    
    try:
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        # Standardize column names
        df.columns = [c.strip().lower() for c in df.columns]
        reviews_data = df.to_dict(orient="records")
        return compute_metrics(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing file: {str(e)}")

@app.get("/")
async def serve_index():
    if os.path.exists("frontend/index.html"):
        with open("frontend/index.html", "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    return HTMLResponse(content="Frontend not found", status_code=404)
