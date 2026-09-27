# Hotel Review Visualization and Analysis Dashboard

A modern full-stack web application designed to collect, visualize, and analyze hotel customer reviews with built-in automated sentiment categorization.

## Project Architecture
- **Backend**: Python 3.10+, FastAPI, Pytest, Uvicorn
- **Frontend**: Single-page application using Tailwind CSS (via CDN) and Chart.js
- **Containerization**: Docker & Docker Compose

## Quick Start with Docker

1. Ensure Docker and Docker Compose are installed on your machine.
2. Run the following command from the root directory:
   ```bash
   docker-compose up --build
   ```
3. The backend API will be available at `http://localhost:8000`.
4. Open `frontend/index.html` directly in your web browser to interact with the dashboard.

## Local Development (Without Docker)

### Backend Setup
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
