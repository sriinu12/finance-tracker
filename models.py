# models.py
# Description: Defines data models for the project, including the Transaction class.

class Transaction:
    def __init__(self, date, amount, category, description):
        self.date = date          # Expected format: "YYYY-MM-DD"
        self.amount = amount      # Float: positive for income, negative for expense
        self.category = category  # String representing the transaction category
        self.description = description  # String description of the transaction

    def to_dict(self):
        """Return a dictionary representation of the transaction."""
        return {
            "date": self.date,
            "amount": self.amount,
            "category": self.category,
            "description": self.description
        }
