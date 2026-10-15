# ADR 0001: Keep pricing operations in services

Status: Accepted

## Context

This Python project already keeps application operations and pure policies in
`services/`, with transport decoding and response formatting in `handlers/`.
The JSON quote handler is an existing entry point; a CLI price preview is a
prospective second entry point for the same pricing behavior.

## Decision

Keep `discount_rate(tier)` in `services/discounts.py` as a pure policy returning
Decimal rates: `standard` is `0`, `member` is `0.05`, and unknown tiers raise
`ValueError`.

Keep `quote_total(amount, tier)` in `services/order_total.py` as the shared
application operation. It rejects negative Decimal amounts, applies
`amount * (1 - discount_rate(tier))`, and quantizes the result to `0.01` with
`ROUND_HALF_UP`. Every entry point must preserve these same tier and rounding
rules by calling this operation rather than reimplementing them.

Keep `handle_quote(body)` in `handlers/quote.py` responsible only for JSON
transport conversion and delegation. A future CLI should likewise parse input,
call `quote_total`, and format output; it should not own pricing policies.

Do not add a separate `domain/` directory unless a concrete need emerges from
this project. Do not import Go-style `domain/` and `app/` layout conventions into
this Python codebase merely because another project uses them.

## Consequences

Pricing stays pure, dependency-free, and testable independently of transports.
Sharing `quote_total` prevents the JSON handler and future CLI from drifting on
discounts, invalid tiers, negative amounts, or half-cent rounding. Any later
boundary change must be justified by actual project requirements.
