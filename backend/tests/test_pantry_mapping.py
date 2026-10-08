"""Tests for the core-logic pantry mapping (app/pantry_mapping.py).

These currently fail with NotImplementedError - that's expected per the
brief's TDD rule. Implement compute_expiration_date and
map_items_to_pantry_rows to make these pass.
"""

from datetime import date
from decimal import Decimal

from app.pantry_mapping import compute_expiration_date, map_items_to_pantry_rows
from app.schemas import ExtractedItem


def test_compute_expiration_date_is_after_purchase_date():
    purchased_at = date(2026, 1, 5)
    result = compute_expiration_date("Produce", purchased_at)
    assert result > purchased_at


def test_compute_expiration_date_returns_a_date():
    result = compute_expiration_date("Dairy", date(2026, 1, 5))
    assert isinstance(result, date)


def test_map_items_to_pantry_rows_preserves_decimal_quantity():
    items = [
        ExtractedItem(
            raw_text="1.23 lb @ $2.99/lb",
            name="Bananas",
            category="Produce",
            quantity=Decimal("1.23"),
            unit="lb",
            price=Decimal("3.68"),
        )
    ]
    rows = map_items_to_pantry_rows(receipt_id=1, items=items, purchased_at=date(2026, 1, 5))
    assert len(rows) == 1
    assert rows[0].quantity == Decimal("1.23")
    assert isinstance(rows[0].quantity, Decimal)
    assert rows[0].expiration_date > date(2026, 1, 5)


def test_map_items_to_pantry_rows_excludes_household_items():
    """Per docs/brief.md: Household-tagged items are excluded from the pantry by default."""
    items = [
        ExtractedItem(
            raw_text="PPR TOWEL",
            name="Paper Towels",
            category="Household",
            quantity=Decimal(1),
            unit="each",
            price=Decimal("12.99"),
        )
    ]
    rows = map_items_to_pantry_rows(receipt_id=1, items=items, purchased_at=date(2026, 1, 5))
    assert rows == []
