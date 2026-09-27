# Hotel Review Visualization and Analysis Dashboard

A full-stack web application providing automated sentiment analysis, visualizations, and management for hotel reviews.

## Tech Stack
- **Backend**: FastAPI (Python 3.10), Pydantic, Pytest
- **Frontend**: Tailwind CSS, Chart.js, HTML5
- **Containerization**: Docker & Docker Compose

---

## Quick Start with Docker
Ensure you have Docker and Docker Compose installed.

```bash
docker-compose up --build
```

- **Backend API**: http://localhost:8000
- **API Documentation (Swagger)**: http://localhost:8000/docs
- **Frontend**: Open `frontend/index.html` directly in any web browser.

---

## Local Development (Without Docker)

### 1. Run the Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### 2. Run Tests
```bash
cd backend
pytest
```

### 3. Open Frontend
Open `frontend/index.html` in your browser. (Make sure the backend is running on port 8000).
