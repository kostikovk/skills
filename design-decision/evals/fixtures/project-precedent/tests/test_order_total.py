import unittest
from decimal import Decimal

from handlers.quote import handle_quote
from services.discounts import discount_rate
from services.order_total import quote_total


class DiscountRateTests(unittest.TestCase):
    def test_discount_rates(self):
        cases = (
            ("member_discount", "member", "0.05"),
            ("standard_has_no_discount", "standard", "0"),
        )

        for name, tier, expected_text in cases:
            with self.subTest(case=name):
                # Arrange
                expected = Decimal(expected_text)

                # Act
                actual = discount_rate(tier)

                # Assert
                self.assertEqual(actual, expected)

    def test_unknown_tier_is_rejected(self):
        # Arrange
        tier = "guest"
        expected_message = "Unknown tier: guest"

        # Act
        with self.assertRaises(ValueError) as raised:
            discount_rate(tier)

        # Assert
        self.assertEqual(str(raised.exception), expected_message)


class OrderTotalTests(unittest.TestCase):
    def test_quote_totals(self):
        cases = (
            ("member_discount", "100", "member", "95.00"),
            ("member_total_rounds_up", "10.10", "member", "9.60"),
            ("standard_total", "100", "standard", "100.00"),
            ("standard_half_cent_rounds_up", "10.005", "standard", "10.01"),
            ("zero_total", "0", "standard", "0.00"),
        )

        for name, amount_text, tier, expected_text in cases:
            with self.subTest(case=name):
                # Arrange
                amount = Decimal(amount_text)
                expected = Decimal(expected_text)

                # Act
                actual = quote_total(amount, tier)

                # Assert
                self.assertEqual(actual, expected)

    def test_invalid_inputs_are_rejected(self):
        cases = (
            ("negative_amount", "-0.01", "standard", "Amount must be nonnegative"),
            ("unknown_tier", "10", "guest", "Unknown tier: guest"),
        )

        for name, amount_text, tier, expected_message in cases:
            with self.subTest(case=name):
                # Arrange
                amount = Decimal(amount_text)

                # Act
                with self.assertRaises(ValueError) as raised:
                    quote_total(amount, tier)

                # Assert
                self.assertEqual(str(raised.exception), expected_message)


class QuoteHandlerTests(unittest.TestCase):
    def test_quote_responses(self):
        cases = (
            ("member_quote", '{"amount": "10.10", "tier": "member"}', "9.60"),
            ("standard_quote", '{"amount": "10", "tier": "standard"}', "10.00"),
        )

        for name, body, expected_amount in cases:
            with self.subTest(case=name):
                # Arrange
                expected = {"amount": expected_amount}

                # Act
                actual = handle_quote(body)

                # Assert
                self.assertEqual(actual, expected)


if __name__ == "__main__":
    unittest.main()
