"""FastAPI app entrypoint.

Boilerplate - not core logic.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import pantry, receipts

app = FastAPI(title="ShelfLife AI")

# Week 1: wide-open CORS for local dev (Next.js on localhost:3000).
# Tighten this before any public deploy (Phase 4 - auth/rate limiting).
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(receipts.router)
app.include_router(pantry.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
