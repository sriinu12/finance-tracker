import unittest

from models import Transaction


class TestTransaction(unittest.TestCase):
    def test_to_dict_round_trip(self) -> None:
        txn = Transaction("2025-01-01", 1500, "Salary", "January payout")
        loaded = Transaction.from_dict(txn.to_dict())
        self.assertEqual(loaded.date, "2025-01-01")
        self.assertEqual(loaded.amount, 1500.0)
        self.assertEqual(loaded.category, "Salary")
        self.assertEqual(loaded.description, "January payout")

    def test_validation(self) -> None:
        with self.assertRaises(ValueError):
            Transaction("", 100, "Food", "Lunch")


if __name__ == "__main__":
    unittest.main()
