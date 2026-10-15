"""Pure discount policy shared by pricing operations."""

from decimal import Decimal


def discount_rate(tier: str) -> Decimal:
    if tier == "standard":
        return Decimal("0")
    if tier == "member":
        return Decimal("0.05")
    raise ValueError(f"Unknown tier: {tier}")
