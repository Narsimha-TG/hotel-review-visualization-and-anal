# Hotel Review Visualization and Analysis Dashboard

A production-ready full-stack application featuring a FastAPI backend with automated sentiment analysis, analytics aggregations, test suites, and a responsive Tailwind CSS dashboard with Chart.js visualizations.

## Project Structure

- `backend/`: FastAPI application, dependencies, Dockerfile, and pytest suite.
- `frontend/`: Modern Tailwind CSS responsive dashboard.
- `docker-compose.yml`: Multi-container orchestration configuration.

---

## Quick Start with Docker Compose

Make sure you have Docker and Docker Compose installed.

```bash
docker-compose up --build
```

The backend API will be available at `http://localhost:8000`.
Interactive API documentation (Swagger UI) is available at `http://localhost:8000/docs`.

---

## Running Locally Without Docker

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Run API server
uvicorn main:app --reload --port 8000
```

### 2. Running Tests

```bash
cd backend
pytest
```

### 3. Frontend Setup

Simply open `frontend/index.html` in your web browser or serve it via a static file server (e.g. `npx serve frontend`).
