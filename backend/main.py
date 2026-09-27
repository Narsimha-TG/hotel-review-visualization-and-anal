from fastapi import FastAPI, status
from typing import List, Dict

app = FastAPI()

@app.get("/api/health")
def health_check():
    return {"status": "ok"}

@app.post("/api/reviews", status_code=status.HTTP_201_CREATED)
def add_review(review: Dict):
    return {"message": "Review created successfully"}

@app.get("/api/analytics")
def get_analytics():
    return {"data": "analytics_results"}