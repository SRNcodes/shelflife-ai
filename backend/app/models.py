"""SQLAlchemy models for the Week 1 slice.

Boilerplate - not core logic. This is a deliberately trimmed subset of the
full schema in docs/brief.md: no receipt_discounts, store_abbreviations, or
shelf_life_rules tables yet. Those arrive in Phase 2 alongside the eval work.
"""

import enum
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.db import Base


class ReceiptStatus(str, enum.Enum):
    PROCESSING = "processing"
    PARSED = "parsed"
    NEEDS_REVIEW = "needs_review"
    CONFIRMED = "confirmed"
    FAILED = "failed"


class PantryItemStatus(str, enum.Enum):
    ACTIVE = "active"
    CONSUMED = "consumed"
    EXPIRED = "expired"
    WASTED = "wasted"


class Receipt(Base):
    __tablename__ = "receipts"

    id: Mapped[int] = mapped_column(primary_key=True)
    image_path: Mapped[str] = mapped_column(String(512))
    status: Mapped[ReceiptStatus] = mapped_column(
        Enum(ReceiptStatus, name="receipt_status", native_enum=False),
        default=ReceiptStatus.PROCESSING,
    )
    error_message: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    pantry_items: Mapped[list["PantryItem"]] = relationship(back_populates="receipt")


class PantryItem(Base):
    __tablename__ = "pantry_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    receipt_id: Mapped[int | None] = mapped_column(ForeignKey("receipts.id"), nullable=True)

    name: Mapped[str] = mapped_column(String(255))
    raw_text: Mapped[str] = mapped_column(String(255))
    quantity: Mapped[Decimal] = mapped_column(Numeric(10, 3))
    unit: Mapped[str] = mapped_column(String(32))
    price: Mapped[Decimal | None] = mapped_column(Numeric(10, 2), nullable=True)

    purchased_at: Mapped[date | None] = mapped_column(Date, nullable=True)
    expiration_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    status: Mapped[PantryItemStatus] = mapped_column(
        Enum(PantryItemStatus, name="pantry_item_status", native_enum=False),
        default=PantryItemStatus.ACTIVE,
    )

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    receipt: Mapped[Receipt | None] = relationship(back_populates="pantry_items")
