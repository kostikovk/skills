"""Existing JSON transport caller for the shared pricing operation."""

import json
from decimal import Decimal

from services.order_total import quote_total


def handle_quote(body: str) -> dict[str, str]:
    payload = json.loads(body)
    total = quote_total(Decimal(payload["amount"]), payload["tier"])
    return {"amount": str(total)}
