# ShelfLife AI — Week 1 Slice Design

Status: approved (conversational)
Date: 2026-10-08

## Goal

A rough, ugly, end-to-end loop: upload a receipt photo → Claude vision
extracts structured items → user sees an editable list → confirmed items
save to Postgres as pantry rows → a reminder surfaces for items expiring
soon. No queue, no auth, no Docker beyond a single Postgres service — those
arrive in later phases per `docs/brief.md`.

## Decisions (from brainstorming)

- **Reminder mechanism:** on-demand endpoint (`GET /pantry/expiring-soon`)
  computed live from the DB at request time; frontend shows a banner when
  the pantry page loads. No scheduler/Celery yet.
- **Image storage:** local filesystem (`backend/uploads/`), path stored in
  the `receipts` row. Swappable for S3 later without touching extraction
  logic.
- **Local Postgres:** Docker Compose with a single `postgres` service.
  Multi-service compose (API, worker, Redis) is Phase 3/4.
- **Project location:** `~/projects/shelflife-ai`, fresh git repo, not
  pushed to GitHub yet (local commits only for now).

## Repo layout

```
shelflife-ai/
  docs/
    brief.md
    superpowers/specs/2026-10-08-week1-slice-design.md
  backend/
    app/
      main.py                  # FastAPI app, CORS
      models.py                # SQLAlchemy models: Receipt, PantryItem
      schemas.py                # Pydantic schemas (core logic — stubbed)
      db.py                    # engine/session setup
      extraction.py             # Claude vision call (core logic — stubbed)
      pantry_mapping.py         # parsed item -> pantry row + expiration math (core logic — stubbed)
      routers/
        receipts.py             # POST /receipts, PATCH /receipts/{id}/confirm
        pantry.py                # GET /pantry, GET /pantry/expiring-soon
    alembic/                    # migrations
    tests/                      # pytest; tests for stubbed modules
    uploads/                    # local image storage (gitignored)
    .env.example
    docker-compose.yml           # postgres only
    pyproject.toml / requirements
  frontend/
    app/
      page.tsx                  # upload + editable extracted-items list + pantry/banner view
    package.json
  .gitignore
```

## Data flow

1. `POST /receipts` (multipart upload) — backend saves the image to
   `backend/uploads/`, calls `extraction.py` (stub; raises
   `NotImplementedError` until implemented) to get structured items, stores
   a `receipts` row (`status=parsed` or `status=failed` on error), returns
   the extracted items to the frontend.
2. Frontend renders items as a plain editable table (no component library —
   "ugly is fine" per the brief).
3. `PATCH /receipts/{id}/confirm` — takes the (possibly edited) item list,
   calls `pantry_mapping.py` (stub) to turn each item into a `PantryItem`
   row including expiration date, persists them, sets receipt
   `status=confirmed`.
4. `GET /pantry/expiring-soon` — queries `pantry_items` where
   `expiration_date` falls within N days of today; frontend shows a banner
   if the result is non-empty.

## Data model (Week 1 subset)

Deliberately a trimmed subset of the brief's full schema — no
`store_abbreviations`, `shelf_life_rules`, or `receipt_discounts` tables
yet. Those land in Phase 2 with the eval/accuracy work.

- `receipts`: id, image_path, status (`processing|parsed|needs_review|confirmed|failed`), created_at
- `pantry_items`: id, receipt_id (nullable FK), name, raw_text, quantity (`NUMERIC`), unit, price (`NUMERIC`, nullable), purchased_at, expiration_date, status (`active|consumed|expired|wasted`)

`NUMERIC` (not float) for quantity and price, per the brief.

## Division of labor

Per `docs/brief.md`'s "Working with Claude Code" rules:

- **Claude builds (boilerplate):** project scaffolding, FastAPI app + CORS
  setup, SQLAlchemy models, Alembic migration, router plumbing, Next.js
  scaffold, Docker Compose (Postgres only), `.env.example`, pytest
  fixtures/harness.
- **Srithan writes (core logic), Claude only stubs + tests:**
  - `schemas.py` — Pydantic field definitions for extracted items
  - `extraction.py` — the extraction prompt and `AsyncAnthropic` vision call
  - `pantry_mapping.py` — parsed item → `PantryItem` row mapping, including
    expiration-date math

Stubs carry full signatures, docstrings, and `raise NotImplementedError`.
Tests are written against the intended behavior and will fail until the
core logic is implemented — this is intentional per the brief's TDD rule.

## Testing

pytest with an in-memory SQLite test DB for speed (Postgres-specific
features aren't exercised yet). Tests exist for the stubbed modules
asserting expected shape/behavior, and for the boilerplate (routes, models)
which Claude implements directly.

## Error handling

Extraction failures set the receipt's `status=failed` and store the error
message. No retry logic yet — retries belong to the Phase 3 job queue.

## Out of scope for Week 1 (explicitly deferred)

- Auth, rate limiting, demo mode (Phase 4)
- Redis/Celery async job queue, scheduled daily expiration job (Phase 3)
- Discount/non-food handling, subtotal self-check, store abbreviation
  learning, eval set (Phase 2)
- GitHub push (local commits only until the user pushes)
