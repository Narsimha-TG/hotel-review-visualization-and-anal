# Hotel Review Visualization and Analysis Dashboard

A full-stack web application built with FastAPI, Tailwind CSS, and Chart.js designed to monitor, analyze, and visualize hotel guest reviews and sentiment data.

## Project Architecture
- **Backend**: FastAPI (Python 3.10+) with automatic sentiment classification, analytics aggregation, and Pytest test suite.
- **Frontend**: Responsive Tailwind CSS dashboard equipped with Chart.js analytics visualizations.
- **Orchestration**: Docker Compose running backend FastAPI service and Nginx frontend service.

## Quick Start with Docker Compose
Ensure you have Docker and Docker Compose installed on your machine.

1. Run the multi-container stack:
   ```bash
   docker-compose up --build
   ```
2. Access the Dashboard:
   - Frontend UI: `http://localhost`
   - Backend API Docs (Swagger): `http://localhost:8000/docs`

## Running Locally Without Docker

### 1. Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
Run unit tests:
```bash
pytest
```

### 2. Frontend Setup
Serve the `frontend/index.html` file using any static file server or open it directly in your web browser (ensure the backend is active at `http://localhost:8000`).
