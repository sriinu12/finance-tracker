# tests/test_storage.py
# Description: Unit tests for CSV and JSON storage functions.

import os
import unittest
from storage import save_transactions_to_csv, load_transactions_from_csv, save_transactions_to_json, load_transactions_from_json

class TestStorageCSV(unittest.TestCase):
    def setUp(self):
        self.transactions = [
            {"date": "2025-01-01", "amount": 100.0, "category": "Salary", "description": "January salary"},
            {"date": "2025-01-02", "amount": -50.0, "category": "Groceries", "description": "Supermarket"}
        ]
        self.test_csv = "test_transactions.csv"
        self.test_json = "test_transactions.json"

    def tearDown(self):
        if os.path.exists(self.test_csv):
            os.remove(self.test_csv)
        if os.path.exists(self.test_json):
            os.remove(self.test_json)

    def test_csv_save_and_load(self):
        save_transactions_to_csv(self.transactions, filename=self.test_csv)
        loaded = load_transactions_from_csv(filename=self.test_csv)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0]['category'], "Salary")

    def test_json_save_and_load(self):
        save_transactions_to_json(self.transactions, filename=self.test_json)
        loaded = load_transactions_from_json(filename=self.test_json)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[1]['description'], "Supermarket")

if __name__ == '__main__':
    unittest.main()
