"""SQLAlchemy engine/session setup.

Boilerplate - not core logic. Synchronous session on purpose for Week 1:
the only genuinely async work is the Claude vision call in extraction.py.
Revisit if later phases need true async DB access (e.g. under real
concurrent load from the Celery worker in Phase 3).
"""

from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings

engine = create_engine(settings.database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency that yields a DB session and closes it after the request."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
