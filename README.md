# Hotel Review Visualization and Analysis Dashboard

A modern, production-ready full-stack application for visualizing and analyzing hotel guest reviews with automated sentiment classification.

## Tech Stack
- **Backend**: FastAPI, Pydantic, Uvicorn, Pytest
- **Frontend**: Tailwind CSS, HTML5, Vanilla JavaScript
- **Containerization**: Docker & Docker Compose

## Project Structure
```text
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py
│   └── test_api.py
├── frontend/
│   └── index.html
├── docker-compose.yml
└── README.md
```

## Running with Docker (Recommended)
Make sure you have Docker and Docker Compose installed.

```bash
docker-compose up --build
```

- Access the **Frontend Dashboard**: [http://localhost](http://localhost)
- Access the **Backend API Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)

## Running Locally Without Docker

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Running Tests
```bash
pytest backend/test_api.py
```

### Frontend Setup
Open `frontend/index.html` in your browser or serve it via a simple HTTP server (e.g., `python3 -m http.server 3000` from the `frontend/` directory).
