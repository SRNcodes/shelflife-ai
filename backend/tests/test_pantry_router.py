"""Tests for the pantry router (app/routers/pantry.py) - boilerplate, should
pass as-is.
"""

from datetime import date, timedelta
from decimal import Decimal

from app.models import PantryItem, PantryItemStatus


def _add_item(db_session, *, name, expiration_date, status=PantryItemStatus.ACTIVE):
    item = PantryItem(
        name=name,
        raw_text=name,
        quantity=Decimal(1),
        unit="each",
        price=Decimal("2.50"),
        purchased_at=date.today(),
        expiration_date=expiration_date,
        status=status,
    )
    db_session.add(item)
    db_session.commit()
    return item


def test_list_pantry_returns_active_items(client, db_session):
    _add_item(db_session, name="Milk", expiration_date=date.today() + timedelta(days=10))
    _add_item(
        db_session,
        name="Old Yogurt",
        expiration_date=date.today(),
        status=PantryItemStatus.CONSUMED,
    )

    response = client.get("/pantry")
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Milk"]


def test_expiring_soon_returns_items_within_window(client, db_session):
    _add_item(db_session, name="Yogurt", expiration_date=date.today() + timedelta(days=1))
    _add_item(db_session, name="Canned Beans", expiration_date=date.today() + timedelta(days=365))

    response = client.get("/pantry/expiring-soon")
    assert response.status_code == 200
    names = [item["name"] for item in response.json()]
    assert names == ["Yogurt"]


def test_expiring_soon_empty_when_nothing_expiring(client):
    response = client.get("/pantry/expiring-soon")
    assert response.status_code == 200
    assert response.json() == []
