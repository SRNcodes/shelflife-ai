"""Mapping from extracted receipt items to pantry rows, including expiration
date math.

CORE LOGIC - YOURS TO WRITE (see docs/brief.md).

Week 1 note: there's no shelf_life_rules table yet (that's seeded from USDA
FoodKeeper data in Phase 2). Decide for yourself how to compute a Week-1
expiration date - e.g. a small in-memory category -> days dict as a
placeholder you'll later replace with the DB-backed lookup. Whatever you
pick, document the assumption in your implementation.
"""

from datetime import date

from app.models import PantryItem
from app.schemas import ExtractedItem


def compute_expiration_date(category: str, purchased_at: date) -> date:
    """Compute an expiration date for an item given its category and purchase date.

    Args:
        category: the item's category (e.g. "Produce", "Dairy", "Household").
        purchased_at: the date the item was purchased.

    Returns:
        date: the computed expiration date. Must be strictly after purchased_at.

    Raises:
        NotImplementedError: stub - implement your shelf-life logic here.
    """
    raise NotImplementedError("Implement expiration-date math (see docs/brief.md)")


def map_items_to_pantry_rows(
    receipt_id: int, items: list[ExtractedItem], purchased_at: date
) -> list[PantryItem]:
    """Convert parsed receipt items into PantryItem rows.

    Args:
        receipt_id: the Receipt this batch of items came from.
        items: extracted items (already possibly edited by the user in the UI).
        purchased_at: the receipt's purchase date.

    Returns:
        list[PantryItem]: unsaved ORM objects ready to be added to a session
        and committed. Each row's expiration_date should come from
        compute_expiration_date. Decide how you want to handle Household-
        tagged items here (per docs/brief.md, they're excluded from the
        pantry by default) and how quantity/price (Decimal, never float)
        carry over from the extracted item.

    Raises:
        NotImplementedError: stub - implement the mapping here.
    """
    raise NotImplementedError("Implement item -> pantry row mapping (see docs/brief.md)")
