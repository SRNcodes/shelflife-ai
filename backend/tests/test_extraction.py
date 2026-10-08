"""Placeholder test for the core-logic Claude vision call (app/extraction.py).

Mocking the Anthropic client here would lock in assumptions about how you
structure the call before you've written it. Replace this test once you've
implemented extract_receipt_items: mock `anthropic.AsyncAnthropic` (or
whatever client construction you land on) to return a canned tool-use
response, and assert it's parsed into the correct ExtractedReceipt.
"""

import pytest

from app.extraction import extract_receipt_items


@pytest.mark.asyncio
async def test_extract_receipt_items_not_yet_implemented(tmp_path):
    image_path = tmp_path / "receipt.jpg"
    image_path.write_bytes(b"fake-image-bytes")

    with pytest.raises(NotImplementedError):
        await extract_receipt_items(str(image_path))
