"""Pydantic schemas for extracted receipt data.

CORE LOGIC - YOURS TO WRITE (see docs/brief.md). This file only sketches the
shape; fill in the actual fields, types, and validators yourself.

Why this matters for the interview story: this is the contract between
"whatever Claude's vision call returns" and the rest of the system. Getting
the field types right here (Decimal for quantity/price, not float) is what
makes the self-check and the eval script meaningful later.
"""

from pydantic import BaseModel


class ExtractedItem(BaseModel):
    """A single parsed line item from a receipt.

    TODO(you): define fields. At minimum, per docs/brief.md, you'll need
    something like: raw_text (the literal receipt line), name (cleaned-up
    item name), category, quantity (Decimal - supports weighed items like
    "1.23 lb"), unit, and price (Decimal, line total paid).

    Think about: should category be a free string or a constrained enum?
    How do you represent "this is a discount line, not an item" - a
    separate model, or a flag on this one?
    """


class ExtractedReceipt(BaseModel):
    """The full structured output of one receipt extraction call.

    TODO(you): define fields. Per docs/brief.md you'll need at least: store,
    purchase date, subtotal, tax, total (all as Decimal), and a list of
    ExtractedItem. Consider where discount lines live - a separate list, or
    folded into items.

    This is also the shape your subtotal self-check (item prices minus
    discounts vs. printed subtotal) will validate against.
    """
