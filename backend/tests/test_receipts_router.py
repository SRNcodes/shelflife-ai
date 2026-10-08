"""Tests for the receipts router (app/routers/receipts.py) - boilerplate.

Only tests the wiring paths that don't depend on core logic being
implemented yet: the extraction-failure path (upload) and the
receipt-not-found path (confirm). Once extraction.py and
pantry_mapping.py are implemented, add a happy-path test for each.
"""

import io

from app.models import Receipt, ReceiptStatus


def test_upload_receipt_marks_failed_when_extraction_not_implemented(client, db_session):
    """extract_receipt_items is currently a stub, so upload should surface
    a 502 and leave the receipt marked failed with the error recorded."""
    fake_image = io.BytesIO(b"fake-image-bytes")

    response = client.post("/receipts", files={"file": ("receipt.jpg", fake_image, "image/jpeg")})

    assert response.status_code == 502
    receipt = db_session.query(Receipt).one()
    assert receipt.status == ReceiptStatus.FAILED
    assert receipt.error_message is not None


def test_confirm_receipt_404_when_not_found(client):
    response = client.patch("/receipts/999/confirm", json=[])
    assert response.status_code == 404
