"""Claude vision call that extracts structured items from a receipt image.

CORE LOGIC - YOURS TO WRITE (see docs/brief.md).

Use the async Anthropic client (`anthropic.AsyncAnthropic`) since this is
called from an async FastAPI route. Use a current Claude model string (not
a retired 3.x one) and a max_tokens large enough for long receipts. Start
with forced tool use (tool_choice) to get structured output - the brief
also asks you to check current docs for native structured outputs and
compare both in the eval later (Phase 2), so don't over-invest in one
approach here.
"""

from app.schemas import ExtractedReceipt


async def extract_receipt_items(image_path: str) -> ExtractedReceipt:
    """Extract structured line items from a receipt image via Claude vision.

    Args:
        image_path: Path to the receipt image on local disk (see
            app.config.settings.upload_dir).

    Returns:
        ExtractedReceipt: structured items, store/date, and totals parsed
        from the receipt.

    Raises:
        NotImplementedError: stub - implement the Claude API call here.

    Design questions to resolve as you implement this (for your own notes,
    not graded): how do you read + encode the image for the API? What's
    your prompt asking the model to do with ambiguous abbreviations,
    weighed items, and discount lines? What happens on a malformed/empty
    response - does this function raise, or return a receipt flagged
    needs_review?
    """
    raise NotImplementedError("Implement the Claude vision extraction call (see docs/brief.md)")
