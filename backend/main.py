from fastapi import FastAPI, Query, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict
from datetime import datetime, date
import re
from collections import Counter

app = FastAPI(
    title="Hotel Review Visualization and Analysis API",
    version="1.0.0",
    description="API for analyzing hotel guest feedback, sentiment, aspect ratings, and trends."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Models ---
class AspectRatings(BaseModel):
    cleanliness: float = Field(..., ge=1.0, le=5.0)
    service: float = Field(..., ge=1.0, le=5.0)
    location: float = Field(..., ge=1.0, le=5.0)
    value: float = Field(..., ge=1.0, le=5.0)
    amenities: float = Field(..., ge=1.0, le=5.0)
    dining: float = Field(..., ge=1.0, le=5.0)

class ReviewCreate(BaseModel):
    hotel_id: str
    author_name: str
    rating: float = Field(..., ge=1.0, le=5.0)
    title: str
    comment: str
    stay_type: str = "Leisure"
    room_type: str = "Deluxe King"
    aspects: Optional[AspectRatings] = None

class Review(ReviewCreate):
    id: int
    date: str
    sentiment: str
    sentiment_score: float
    aspects: AspectRatings

class Hotel(BaseModel):
    id: str
    name: str
    location: str
    stars: int

# --- In-memory dataset ---
HOTELS: List[Hotel] = [
    Hotel(id="grand-palace", name="Grand Palace Resort & Spa", location="Maui, Hawaii", stars=5),
    Hotel(id="urban-boutique", name="Aura Urban Boutique Hotel", location="Downtown Chicago", stars=4),
    Hotel(id="alpine-lodge", name="Snowcreek Alpine Lodge", location="Aspen, Colorado", stars=4)
]

def compute_sentiment(text: str, rating: float) -> (str, float):
    positive_words = {"excellent", "amazing", "great", "loved", "superb", "friendly", "clean", "spacious", "delicious", "wonderful", "fantastic", "perfect", "best", "luxury", "breathtaking"}
    negative_words = {"terrible", "dirty", "slow", "bad", "poor", "noisy", "broken", "rude", "awful", "disappointing", "horrible", "stale", "overpriced", "uncomfortable", "cold"}
    
    words = re.findall(r'\w+', text.lower())
    pos_count = sum(1 for w in words if w in positive_words)
    neg_count = sum(1 for w in words if w in negative_words)
    
    # Blend text signal with normalized star rating
    rating_score = (rating - 3.0) / 2.0
    text_score = 0.0
    if (pos_count + neg_count) > 0:
        text_score = (pos_count - neg_count) / (pos_count + neg_count)
    
    combined_score = round(max(-1.0, min(1.0, (rating_score * 0.7) + (text_score * 0.3))), 2)
    
    if combined_score >= 0.2:
        sentiment = "positive"
    elif combined_score <= -0.2:
        sentiment = "negative"
    else:
        sentiment = "neutral"
        
    return sentiment, combined_score

SAMPLE_REVIEWS = [
    {
        "id": 1,
        "hotel_id": "grand-palace",
        "author_name": "Sarah Jenkins",
        "rating": 5.0,
        "title": "Unforgettable tropical getaway!",
        "comment": "The ocean view was breathtaking. Superb staff, impeccably clean rooms, and delicious dining options by the pool.",
        "stay_type": "Leisure",
        "room_type": "Oceanfront Suite",
        "date": "2024-03-12",
        "sentiment": "positive",
        "sentiment_score": 0.95,
        "aspects": {"cleanliness": 5.0, "service": 5.0, "location": 5.0, "value": 4.5, "amenities": 5.0, "dining": 5.0}
    },
    {
        "id": 2,
        "hotel_id": "grand-palace",
        "author_name": "David Miller",
        "rating": 4.0,
        "title": "Great resort, but valet was slow",
        "comment": "Loved the spa and private beach. Breakfast buffet was amazing. Valet was slow during peak departure hours.",
        "stay_type": "Family",
        "room_type": "Two Queen Deluxe",
        "date": "2024-03-05",
        "sentiment": "positive",
        "sentiment_score": 0.65,
        "aspects": {"cleanliness": 4.5, "service": 3.5, "location": 5.0, "value": 4.0, "amenities": 4.5, "dining": 4.5}
    },
    {
        "id": 3,
        "hotel_id": "grand-palace",
        "author_name": "Marcus Vance",
        "rating": 2.0,
        "title": "Noisy AC and overpriced food",
        "comment": "Air conditioning was terribly noisy throughout the night. Front desk was indifferent. Food was overpriced for average quality.",
        "stay_type": "Business",
        "room_type": "Garden King",
        "date": "2024-02-24",
        "sentiment": "negative",
        "sentiment_score": -0.75,
        "aspects": {"cleanliness": 3.0, "service": 2.0, "location": 4.0, "value": 1.5, "amenities": 2.0, "dining": 2.0}
    },
    {
        "id": 4,
        "hotel_id": "grand-palace",
        "author_name": "Elena Rostova",
        "rating": 5.0,
        "title": "Pure luxury and serenity",
        "comment": "Clean, spacious rooms with top tier amenities. Exceptional service from Maria at concierge. Will definitely return!",
        "stay_type": "Leisure",
        "room_type": "Oceanfront Suite",
        "date": "2024-02-14",
        "sentiment": "positive",
        "sentiment_score": 0.9,
        "aspects": {"cleanliness": 5.0, "service": 5.0, "location": 5.0, "value": 4.5, "amenities": 5.0, "dining": 4.5}
    },
    {
        "id": 5,
        "hotel_id": "grand-palace",
        "author_name": "Kevin Patel",
        "rating": 3.0,
        "title": "Decent stay, room needed updates",
        "comment": "Location is unbeatable, but bathroom fixtures were dated. Wi-Fi connection dropped occasionally during work calls.",
        "stay_type": "Business",
        "room_type": "Garden King",
        "date": "2024-01-28",
        "sentiment": "neutral",
        "sentiment_score": 0.05,
        "aspects": {"cleanliness": 3.5, "service": 3.5, "location": 4.5, "value": 3.0, "amenities": 2.5, "dining": 3.0}
    },
    {
        "id": 6,
        "hotel_id": "grand-palace",
        "author_name": "Chloe Bennett",
        "rating": 5.0,
        "title": "Outstanding anniversary weekend",
        "comment": "They surprised us with complimentary champagne. Fantastic infinity pool and serene atmosphere. Unmatched service!",
        "stay_type": "Couple",
        "room_type": "Penthouse Suite",
        "date": "2024-01-10",
        "sentiment": "positive",
        "sentiment_score": 0.95,
        "aspects": {"cleanliness": 5.0, "service": 5.0, "location": 5.0, "value": 4.5, "amenities": 5.0, "dining": 5.0}
    },
    {
        "id": 7,
        "hotel_id": "urban-boutique",
        "author_name": "Liam O'Connor",
        "rating": 4.5,
        "title": "Chic urban vibe in the heart of the city",
        "comment": "Walking distance to everything. Stylish rooms, cozy rooftop lounge, and friendly bartenders.",
        "stay_type": "Leisure",
        "room_type": "Loft Studio",
        "date": "2024-03-01",
        "sentiment": "positive",
        "sentiment_score": 0.8,
        "aspects": {"cleanliness": 4.5, "service": 4.5, "location": 5.0, "value": 4.0, "amenities": 4.0, "dining": 4.5}
    },
    {
        "id": 8,
        "hotel_id": "alpine-lodge",
        "author_name": "Hannah Schmidt",
        "rating": 4.8,
        "title": "Ski-in ski-out perfection",
        "comment": "Warm fireplaces, incredible mountain views, heated outdoor pool. The breakfast skillet was fantastic!",
        "stay_type": "Leisure",
        "room_type": "Cabin Suite",
        "date": "2024-02-18",
        "sentiment": "positive",
        "sentiment_score": 0.9,
        "aspects": {"cleanliness": 5.0, "service": 4.8, "location": 5.0, "value": 4.2, "amenities": 4.8, "dining": 4.7}
    }
]

# Storage state
reviews_store: List[Review] = [Review(**r) for r in SAMPLE_REVIEWS]

# --- Endpoints ---

@app.get("/api/health")
def health():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.get("/api/hotels", response_model=List[Hotel])
def get_hotels():
    return HOTELS

@app.get("/api/overview")
def get_overview(hotel_id: Optional[str] = Query(None)):
    records = [r for r in reviews_store if not hotel_id or r.hotel_id == hotel_id]
    total = len(records)
    if total == 0:
        return {
            "hotel_id": hotel_id,
            "total_reviews": 0,
            "average_rating": 0.0,
            "net_sentiment_score": 0.0,
            "recommendation_rate": 0.0,
            "sentiment_distribution": {"positive": 0, "neutral": 0, "negative": 0},
            "rating_distribution": {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
        }
    
    avg_rating = round(sum(r.rating for r in records) / total, 2)
    sentiments = [r.sentiment for r in records]
    pos_count = sentiments.count("positive")
    neu_count = sentiments.count("neutral")
    neg_count = sentiments.count("negative")
    
    # Net Sentiment Score = (% Positive - % Negative)
    nss = round(((pos_count - neg_count) / total) * 100, 1)
    rec_rate = round((sum(1 for r in records if r.rating >= 4.0) / total) * 100, 1)
    
    rating_dist = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for r in records:
        rounded = int(round(r.rating))
        clamped = max(1, min(5, rounded))
        rating_dist[clamped] += 1
        
    return {
        "hotel_id": hotel_id or "all",
        "total_reviews": total,
        "average_rating": avg_rating,
        "net_sentiment_score": nss,
        "recommendation_rate": rec_rate,
        "sentiment_distribution": {
            "positive": pos_count,
            "neutral": neu_count,
            "negative": neg_count
        },
        "rating_distribution": rating_dist
    }

@app.get("/api/aspects")
def get_aspect_analysis(hotel_id: Optional[str] = Query(None)):
    records = [r for r in reviews_store if not hotel_id or r.hotel_id == hotel_id]
    if not records:
        return {"aspects": {}, "benchmarks": {}}
        
    n = len(records)
    keys = ["cleanliness", "service", "location", "value", "amenities", "dining"]
    aspect_averages = {}
    for k in keys:
        aspect_averages[k] = round(sum(getattr(r.aspects, k) for r in records) / n, 2)
        
    # Benchmarks (industry average standard)
    benchmarks = {
        "cleanliness": 4.2,
        "service": 4.1,
        "location": 4.4,
        "value": 3.8,
        "amenities": 4.0,
        "dining": 3.9
    }
    
    return {
        "aspects": aspect_averages,
        "benchmarks": benchmarks
    }

@app.get("/api/trends")
def get_trends(hotel_id: Optional[str] = Query(None)):
    records = [r for r in reviews_store if not hotel_id or r.hotel_id == hotel_id]
    # Group by month string (YYYY-MM)
    monthly: Dict[str, List[Review]] = {}
    for r in sorted(records, key=lambda x: x.date):
        month_key = r.date[:7]
        monthly.setdefault(month_key, []).append(r)
        
    result = []
    for m_key, r_list in monthly.items():
        avg_r = round(sum(r.rating for r in r_list) / len(r_list), 2)
        avg_s = round(sum(r.sentiment_score for r in r_list) / len(r_list), 2)
        result.append({
            "period": m_key,
            "review_count": len(r_list),
            "average_rating": avg_r,
            "average_sentiment": avg_s
        })
    return result

@app.get("/api/keywords")
def get_keywords(hotel_id: Optional[str] = Query(None)):
    records = [r for r in reviews_store if not hotel_id or r.hotel_id == hotel_id]
    stop_words = {"the", "and", "was", "a", "to", "in", "of", "for", "with", "it", "our", "is", "at", "on", "my", "we", "but", "by", "had", "an", "they", "were", "this"}
    
    topic_counts = Counter()
    topic_ratings = {}
    
    for r in records:
        words = re.findall(r'\b[a-zA-Z]{3,}\b', f"{r.title} {r.comment}".lower())
        for w in words:
            if w not in stop_words:
                topic_counts[w] += 1
                topic_ratings.setdefault(w, []).append(r.rating)
                
    most_common = topic_counts.most_common(12)
    keywords = []
    for word, count in most_common:
        avg_r = round(sum(topic_ratings[word]) / len(topic_ratings[word]), 2)
        sentiment_label = "positive" if avg_r >= 4.0 else ("negative" if avg_r <= 2.5 else "neutral")
        keywords.append({
            "keyword": word,
            "frequency": count,
            "average_rating": avg_r,
            "sentiment": sentiment_label
        })
    return keywords

@app.get("/api/reviews")
def get_reviews(
    hotel_id: Optional[str] = Query(None),
    sentiment: Optional[str] = Query(None),
    min_rating: Optional[float] = Query(None),
    search: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50)
):
    filtered = reviews_store
    if hotel_id and hotel_id != "all":
        filtered = [r for r in filtered if r.hotel_id == hotel_id]
    if sentiment and sentiment != "all":
        filtered = [r for r in filtered if r.sentiment.lower() == sentiment.lower()]
    if min_rating is not None:
        filtered = [r for r in filtered if r.rating >= min_rating]
    if search:
        s_lower = search.lower()
        filtered = [r for r in filtered if (s_lower in r.comment.lower() or s_lower in r.title.lower() or s_lower in r.author_name.lower())]
        
    total_items = len(filtered)
    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    paged = filtered[start_idx:end_idx]
    
    return {
        "total": total_items,
        "page": page,
        "page_size": page_size,
        "reviews": paged
    }

@app.post("/api/reviews", response_model=Review, status_code=status.HTTP_201_CREATED)
def add_review(payload: ReviewCreate):
    sentiment, score = compute_sentiment(f"{payload.title} {payload.comment}", payload.rating)
    
    # Fallback aspect ratings if user didn't specify
    aspects = payload.aspects or AspectRatings(
        cleanliness=payload.rating,
        service=payload.rating,
        location=payload.rating,
        value=payload.rating,
        amenities=payload.rating,
        dining=payload.rating
    )
    
    new_id = max([r.id for r in reviews_store], default=0) + 1
    new_review = Review(
        id=new_id,
        hotel_id=payload.hotel_id,
        author_name=payload.author_name,
        rating=payload.rating,
        title=payload.title,
        comment=payload.comment,
        stay_type=payload.stay_type,
        room_type=payload.room_type,
        date=date.today().isoformat(),
        sentiment=sentiment,
        sentiment_score=score,
        aspects=aspects
    )
    reviews_store.insert(0, new_review)
    return new_review

@app.post("/api/reset")
def reset_data():
    global reviews_store
    reviews_store = [Review(**r) for r in SAMPLE_REVIEWS]
    return {"status": "reset completed", "count": len(reviews_store)}
