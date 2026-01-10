# Thai U.S. Investment Portal - Backend

FastAPI backend for the Thai U.S. Investment Portal.

## Tech Stack

- Python 3.11+
- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- Redis
- yfinance

## Setup

1. Create virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy environment variables:

```bash
cp .env.example .env
# Edit .env with your values
```

4. Run migrations:

```bash
alembic upgrade head
```

5. Start development server:

```bash
uvicorn app.main:app --reload --port 8000
```

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── app/
│   ├── main.py           # FastAPI app
│   ├── config.py         # Settings
│   ├── database.py       # DB connection
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── routers/          # API endpoints
│   ├── services/         # Business logic
│   ├── jobs/             # Scheduled tasks
│   └── utils/            # Helpers
├── alembic/              # Migrations
├── data/                 # Seed data
└── tests/                # Tests
```
