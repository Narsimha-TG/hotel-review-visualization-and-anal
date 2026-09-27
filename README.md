# Hotel Review Visualization and Analysis Dashboard

A full-stack solution featuring a high-performance **FastAPI** backend and a responsive **Tailwind CSS & Chart.js** frontend dashboard for analyzing hotel reviews and sentiment metrics.

## Features
- **RESTful API**: Endpoints for listing, filtering, analyzing, and creating hotel reviews.
- **Sentiment Analysis**: Automatic rule-based sentiment classification (Positive, Neutral, Negative).
- **Interactive Analytics**: Visual charts showing sentiment distributions and average ratings per hotel.
- **Modern UI**: Clean dashboard built with Tailwind CSS and Chart.js.

## Quick Start with Docker
Ensure Docker and Docker Compose are installed on your system.

```bash
docker-compose up --build
```

- Access the **Frontend Dashboard**: `http://localhost`
- Access the **Backend API Docs (Swagger)**: `http://localhost:8000/docs`

## Local Development without Docker

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Running Tests
```bash
cd backend
pytest test_api.py
```

### Frontend
Serve `frontend/index.html` via any static file server or open directly in a browser (ensure backend is running on `http://localhost:8000`).
