# Hotel Review Visualization and Analysis Dashboard

A modern, production-grade Hotel Review Intelligence and Aspect Sentiment Dashboard built with **FastAPI** and a responsive **Tailwind CSS + Chart.js** frontend.

## Features

- **Comprehensive Aspect Sentiment Analysis**: Breaks down guest ratings across six crucial operational pillars: *Cleanliness, Staff & Service, Location, Value for Money, Amenities/Wi-Fi, and Food & Dining*.
- **Industry Benchmark Radar**: Compare property aspect ratings against hospitality standards in real-time.
- **Trend & Sentiment Tracking**: Dual-axis monthly historical tracking of star ratings and synthesized sentiment score (-1 to +1).
- **Topic & Keyword Mining**: Automatically pulls frequent sentiment-tagged topics from qualitative review texts.
- **Filtering & Search**: Live property filtering, sentiment classification (Positive / Neutral / Negative), and instant keyword searching.
- **Submit Reviews**: Dynamic submission modal with multi-aspect sliders and automated sentiment categorization.

---

## Quickstart with Docker Compose

Ensure Docker and Docker Compose are installed, then run:

```bash
docker-compose up --build
```

- **Frontend Dashboard**: [http://localhost:3000](http://localhost:3000)
- **Backend API Docs (Swagger)**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Backend Health Check**: [http://localhost:8000/api/health](http://localhost:8000/api/health)

---

## Local Development Setup

### 1. Backend (FastAPI)
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Frontend
Serve the `frontend` folder with any web server (or open `frontend/index.html` directly in modern browsers):
```bash
cd frontend
python3 -m http.server 3000
```
Navigate to `http://localhost:3000`.

---

## Running Automated Tests

Run the test suite using pytest:
```bash
cd backend
pytest test_api.py -v
```
