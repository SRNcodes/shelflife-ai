"""initial: receipts, pantry_items

Revision ID: 0001
Revises:
Create Date: 2026-10-08
"""

import sqlalchemy as sa

from alembic import op

revision = "0001"
down_revision = None
branch_labels = None
depends_on = None

receipt_status = sa.Enum(
    "processing",
    "parsed",
    "needs_review",
    "confirmed",
    "failed",
    name="receipt_status",
    native_enum=False,
)
pantry_item_status = sa.Enum(
    "active",
    "consumed",
    "expired",
    "wasted",
    name="pantry_item_status",
    native_enum=False,
)


def upgrade() -> None:
    op.create_table(
        "receipts",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("image_path", sa.String(length=512), nullable=False),
        sa.Column("status", receipt_status, nullable=False, server_default="processing"),
        sa.Column("error_message", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        "pantry_items",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("receipt_id", sa.Integer(), sa.ForeignKey("receipts.id"), nullable=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("raw_text", sa.String(length=255), nullable=False),
        sa.Column("quantity", sa.Numeric(10, 3), nullable=False),
        sa.Column("unit", sa.String(length=32), nullable=False),
        sa.Column("price", sa.Numeric(10, 2), nullable=True),
        sa.Column("purchased_at", sa.Date(), nullable=True),
        sa.Column("expiration_date", sa.Date(), nullable=True),
        sa.Column("status", pantry_item_status, nullable=False, server_default="active"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
    )
    op.create_index(
        "ix_pantry_items_user_expiration_status",
        "pantry_items",
        ["expiration_date", "status"],
    )


def downgrade() -> None:
    op.drop_index("ix_pantry_items_user_expiration_status", table_name="pantry_items")
    op.drop_table("pantry_items")
    op.drop_table("receipts")
