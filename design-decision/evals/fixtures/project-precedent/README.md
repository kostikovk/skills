# Project precedent: synthetic eval fixture

This is a small, self-contained **synthetic eval fixture**, not production code.
It provides real Python source, an architectural decision, an existing caller,
and executable tests for checking project-first discovery. It uses only the
Python standard library; the application functions perform no I/O or mutation
of external state. `services/` and `handlers/` are namespace packages.

## Existing project evidence

- [ADR 0001](docs/adr/0001-pricing-boundary.md) records the pricing boundary.
- `services/discounts.py`: `discount_rate(tier)` supplies pure Decimal rates.
- `services/order_total.py`: `quote_total(amount, tier)` applies the discount
  and rounds the total to cents using `ROUND_HALF_UP`.
- `handlers/quote.py`: `handle_quote(body)` decodes a JSON body such as
  `{"amount": "10.10", "tier": "member"}`, calls `quote_total`, and returns
  `{"amount": "9.60"}`. Amounts on the wire are decimal strings.
- `tests/test_order_total.py` exercises the policies, operation, and caller.

## Design scenario

Add a CLI price preview alongside the existing quote handler. The design should
first discover this project's source and ADR, then recommend that the CLI parse
its inputs and invoke the existing `services.order_total.quote_total` operation.
Do not duplicate discounts or rounding, introduce a separate domain directory
without a concrete need, or impose Go-style `domain/` and `app/` directories on
this Python project. No CLI implementation is included: this fixture evaluates
a design recommendation, not feature implementation.

## Run tests

From this fixture's root directory:

```sh
python3 -B -m unittest discover -s tests -v
```

`-B` prevents bytecode-cache writes. No dependencies or setup are required.
