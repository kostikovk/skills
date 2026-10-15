"""Shared pricing operation for transport-independent quotes."""

from decimal import ROUND_HALF_UP, Decimal

from services.discounts import discount_rate


def quote_total(amount: Decimal, tier: str) -> Decimal:
    if amount < Decimal("0"):
        raise ValueError("Amount must be nonnegative")
    total = amount * (Decimal("1") - discount_rate(tier))
    return total.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
