# ShelfLife AI

A multimodal food tracker: upload a receipt photo, Claude vision extracts
structured items, each item gets a shelf life, and reminders fire before
things expire. Full project brief: [`docs/brief.md`](docs/brief.md).

**Status:** Week 1 scaffolding - rough end-to-end loop, core extraction and
pantry-mapping logic not yet implemented (see "Core logic" below).

## Stack

- **Backend:** FastAPI + SQLAlchemy + Alembic, Postgres
- **Frontend:** Next.js (App Router)
- **Vision/LLM:** Claude API (`anthropic.AsyncAnthropic`)

## Running it locally

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
cp .env.example .env   # fill in ANTHROPIC_API_KEY

docker compose up -d        # starts Postgres
alembic upgrade head        # creates tables

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

Visit http://localhost:3000.

### Tests

```bash
cd backend
source .venv/bin/activate
pytest
ruff check app tests
black --check app tests
```

## Core logic (not yet implemented)

Per the project brief, these are intentionally left as stubs
(`NotImplementedError`) with tests already written against them:

- `backend/app/schemas.py` - Pydantic schemas for extracted receipt data
- `backend/app/extraction.py` - the Claude vision extraction call
- `backend/app/pantry_mapping.py` - parsed item → pantry row mapping + expiration math

## Project layout

```
backend/
  app/            FastAPI app, models, routers, core-logic modules
  alembic/        DB migrations
  tests/          pytest
frontend/
  app/            Next.js App Router pages
docs/
  brief.md        full project brief
  superpowers/specs/   design docs
```
