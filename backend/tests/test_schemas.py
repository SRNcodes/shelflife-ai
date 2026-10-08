"""Tests for the core-logic Pydantic schemas (app/schemas.py).

These currently fail because ExtractedItem/ExtractedReceipt have no fields
yet - that's expected per the brief's TDD rule. Implement the schemas to
make these pass.
"""

from datetime import date
from decimal import Decimal

from app.schemas import ExtractedItem, ExtractedReceipt


def test_extracted_item_has_expected_fields():
    item = ExtractedItem(
        raw_text="GV ORG BNNA 2@.69",
        name="Organic Banana",
        category="Produce",
        quantity=Decimal(2),
        unit="each",
        price=Decimal("1.38"),
    )
    assert item.raw_text == "GV ORG BNNA 2@.69"
    assert item.name == "Organic Banana"
    assert item.category == "Produce"
    assert item.quantity == Decimal(2)
    assert item.unit == "each"
    assert item.price == Decimal("1.38")


def test_extracted_item_quantity_is_decimal_not_float():
    """Weighed items like "1.23 lb @ $2.99/lb" need real decimal precision."""
    item = ExtractedItem(
        raw_text="1.23 lb @ $2.99/lb",
        name="Bananas",
        category="Produce",
        quantity=Decimal("1.23"),
        unit="lb",
        price=Decimal("3.68"),
    )
    assert isinstance(item.quantity, Decimal)
    assert isinstance(item.price, Decimal)


def test_extracted_receipt_has_expected_fields():
    receipt = ExtractedReceipt(
        store="Costco",
        purchase_date=date(2026, 1, 5),
        subtotal=Decimal("45.00"),
        tax=Decimal("4.00"),
        total=Decimal("49.00"),
        items=[
            ExtractedItem(
                raw_text="KS RTSRY CHKN",
                name="Rotisserie Chicken",
                category="Meat",
                quantity=Decimal(1),
                unit="each",
                price=Decimal("5.99"),
            )
        ],
    )
    assert receipt.store == "Costco"
    assert receipt.purchase_date == date(2026, 1, 5)
    assert receipt.subtotal == Decimal("45.00")
    assert receipt.total == Decimal("49.00")
    assert len(receipt.items) == 1
    assert receipt.items[0].name == "Rotisserie Chicken"
