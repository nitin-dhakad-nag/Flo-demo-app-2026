import unittest

from bot import RefundBot


class DefendedModeGuardrailTests(unittest.TestCase):
    def test_requested_over_limit_is_denied_even_if_model_recommends_less(self):
        parsed = RefundBot._parse_decision(
            "DECISION: APPROVE\nREFUND_PERCENT: 10\nREASON: Customer request."
        )

        result = RefundBot._enforce_business_rule(
            parsed,
            {"amount": 12000},
            requested_percent=20,
        )

        self.assertEqual(result["decision"], "DENY")
        self.assertEqual(result["percent"], 0.0)

    def test_model_over_limit_is_denied(self):
        parsed = RefundBot._parse_decision(
            "DECISION: APPROVE\nREFUND_PERCENT: 20\nREASON: Packaging damage."
        )

        result = RefundBot._enforce_business_rule(parsed, {"amount": 12000})

        self.assertEqual(result["decision"], "DENY")
        self.assertEqual(result["percent"], 0.0)

    def test_valid_under_limit_approval_is_allowed(self):
        parsed = RefundBot._parse_decision(
            "DECISION: APPROVE\nREFUND_PERCENT: 10\nREASON: Packaging damage."
        )

        result = RefundBot._enforce_business_rule(parsed, {"amount": 12000})

        self.assertEqual(result["decision"], "APPROVE")
        self.assertEqual(result["percent"], 10.0)

    def test_malformed_refund_response_fails_closed(self):
        parsed = RefundBot._parse_decision("I approve a 20% refund.")

        result = RefundBot._enforce_business_rule(parsed, {"amount": 12000})

        self.assertEqual(result["decision"], "DENY")
        self.assertEqual(result["percent"], 0.0)

    def test_denial_never_displays_a_positive_refund(self):
        parsed = RefundBot._parse_decision(
            "DECISION: DENY\nREFUND_PERCENT: 10\nREASON: Not eligible."
        )

        result = RefundBot._enforce_business_rule(parsed, {"amount": 12000})

        self.assertEqual(result["decision"], "DENY")
        self.assertEqual(result["percent"], 0.0)

    def test_requested_percentage_formats_are_detected(self):
        self.assertEqual(RefundBot._requested_percent("I want a 20% refund"), 20.0)
        self.assertEqual(RefundBot._requested_percent("Please refund 12 percent"), 12.0)


if __name__ == "__main__":
    unittest.main()