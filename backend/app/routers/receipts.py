"""Receipt upload and confirmation endpoints.

Boilerplate - not core logic. Wires together extraction.py and
pantry_mapping.py (both of which are stubs until you implement them).
"""

import shutil
import uuid
from datetime import date
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.config import settings
from app.db import get_db
from app.extraction import extract_receipt_items
from app.models import Receipt, ReceiptStatus
from app.pantry_mapping import map_items_to_pantry_rows
from app.schemas import ExtractedItem

router = APIRouter(prefix="/receipts", tags=["receipts"])


@router.post("")
async def upload_receipt(file: UploadFile, db: Session = Depends(get_db)) -> dict:
    """Save the uploaded image, run extraction, and return the parsed items.

    On extraction failure, the receipt is saved with status=failed and the
    error message, and a 502 is returned (the frontend can show "couldn't
    read this receipt, try again").
    """
    upload_dir = Path(settings.upload_dir)
    upload_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(file.filename or "receipt.jpg").suffix or ".jpg"
    dest_path = upload_dir / f"{uuid.uuid4().hex}{suffix}"
    with dest_path.open("wb") as out:
        shutil.copyfileobj(file.file, out)

    receipt = Receipt(image_path=str(dest_path), status=ReceiptStatus.PROCESSING)
    db.add(receipt)
    db.commit()
    db.refresh(receipt)

    try:
        extracted = await extract_receipt_items(str(dest_path))
    except Exception as exc:
        receipt.status = ReceiptStatus.FAILED
        receipt.error_message = str(exc)
        db.commit()
        raise HTTPException(status_code=502, detail=f"Receipt extraction failed: {exc}") from exc

    receipt.status = ReceiptStatus.PARSED
    db.commit()

    return {"receipt_id": receipt.id, "extracted": extracted}


@router.patch("/{receipt_id}/confirm")
def confirm_receipt(
    receipt_id: int,
    items: list[ExtractedItem],
    purchased_at: date | None = None,
    db: Session = Depends(get_db),
) -> dict:
    """Save the (possibly user-edited) item list as pantry rows."""
    receipt = db.get(Receipt, receipt_id)
    if receipt is None:
        raise HTTPException(status_code=404, detail="Receipt not found")

    pantry_rows = map_items_to_pantry_rows(
        receipt_id=receipt.id, items=items, purchased_at=purchased_at or date.today()
    )
    db.add_all(pantry_rows)
    receipt.status = ReceiptStatus.CONFIRMED
    db.commit()

    return {"receipt_id": receipt.id, "pantry_items_created": len(pantry_rows)}
