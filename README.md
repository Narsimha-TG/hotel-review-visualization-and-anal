# Hotel Review Visualization and Analysis Dashboard

A modern full-stack application for capturing, visualizing, and analyzing hotel customer reviews with automated sentiment classification.

## Project Structure

- `backend/`: FastAPI Python application with automated tests and Dockerfile.
- `frontend/`: Responsive Tailwind CSS single-page dashboard utilizing Chart.js.
- `docker-compose.yml`: Multi-container orchestration specification.

## Quick Start with Docker

Ensure you have Docker and Docker Compose installed:

```bash
docker-compose up --build
```

The backend API will be available at `http://localhost:8000`.

## Running the Frontend

Open `frontend/index.html` directly in any web browser or serve via a local static server (e.g., `npx serve frontend`).

## Running Backend Tests

Navigate to the `backend/` directory and execute pytest:

```bash
cd backend
pip install -r requirements.txt
pytest -v
```
