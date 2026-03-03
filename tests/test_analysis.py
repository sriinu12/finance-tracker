import unittest

from analysis import create_income_expense_chart


class TestAnalysis(unittest.TestCase):
    def test_create_income_expense_chart(self) -> None:
        transactions = [
            {"date": "2025-01-01", "amount": 100.0, "category": "Salary", "description": "Salary"},
            {"date": "2025-01-15", "amount": -40.0, "category": "Food", "description": "Dinner"},
            {"date": "2025-02-01", "amount": 200.0, "category": "Salary", "description": "Salary"},
            {"date": "2025-02-10", "amount": -60.0, "category": "Groceries", "description": "Market"},
        ]
        fig = create_income_expense_chart(transactions)
        self.assertIsNotNone(fig)

    def test_create_income_expense_chart_handles_empty_data(self) -> None:
        fig = create_income_expense_chart([])
        self.assertIsNotNone(fig)


if __name__ == "__main__":
    unittest.main()
