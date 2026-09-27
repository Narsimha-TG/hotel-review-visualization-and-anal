# Hotel Review Visualization and Analysis Dashboard

A modern full-stack dashboard built with FastAPI (Backend) and Tailwind CSS / Chart.js (Frontend) for analyzing hotel reviews and visualizing sentiment analytics.

## Project Structure
- `backend/`: FastAPI application, Pydantic models, pytest suite, and Dockerfile.
- `frontend/`: Responsive dashboard featuring live charts and filtering capabilities.
- `docker-compose.yml`: Multi-container orchestration configuration.

## Getting Started

### Running with Docker Compose
Ensure Docker and Docker Compose are installed, then run:
```bash
docker-compose up --build
```
- Backend API & Docs: http://localhost:8000/docs
- Open `frontend/index.html` directly in your browser to access the dashboard.

### Running Locally (Without Docker)

#### 1. Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

#### 2. Running Tests
```bash
cd backend
pytest
```

#### 3. Frontend
Open `frontend/index.html` in any modern web browser.
