"""Pantry listing and expiring-soon reminder endpoints.

Boilerplate - not core logic.
"""

from datetime import date, timedelta

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.models import PantryItem, PantryItemStatus

router = APIRouter(prefix="/pantry", tags=["pantry"])


@router.get("")
def list_pantry(db: Session = Depends(get_db)) -> list[dict]:
    """Return all active pantry items."""
    rows = db.scalars(select(PantryItem).where(PantryItem.status == PantryItemStatus.ACTIVE)).all()
    return [_serialize(row) for row in rows]


@router.get("/expiring-soon")
def expiring_soon(db: Session = Depends(get_db)) -> list[dict]:
    """Return active pantry items expiring within settings.expiring_soon_days.

    Computed live at request time - no scheduler yet (that's Phase 3). The
    frontend polls this on page load to show the reminder banner.
    """
    cutoff = date.today() + timedelta(days=settings.expiring_soon_days)
    rows = db.scalars(
        select(PantryItem)
        .where(PantryItem.status == PantryItemStatus.ACTIVE)
        .where(PantryItem.expiration_date.is_not(None))
        .where(PantryItem.expiration_date <= cutoff)
        .order_by(PantryItem.expiration_date.asc())
    ).all()
    return [_serialize(row) for row in rows]


def _serialize(item: PantryItem) -> dict:
    return {
        "id": item.id,
        "name": item.name,
        "quantity": str(item.quantity),
        "unit": item.unit,
        "price": str(item.price) if item.price is not None else None,
        "expiration_date": item.expiration_date.isoformat() if item.expiration_date else None,
        "status": item.status.value,
    }
