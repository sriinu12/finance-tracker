from __future__ import annotations

import csv
import json
import sqlite3
from pathlib import Path
from typing import Any, TypedDict


class TransactionRecord(TypedDict):
    date: str
    amount: float
    category: str
    description: str


def _normalize_transaction(record: dict[str, Any]) -> TransactionRecord:
    return {
        "date": str(record["date"]),
        "amount": float(record["amount"]),
        "category": str(record["category"]),
        "description": str(record["description"]),
    }


def save_transactions_to_csv(
    transactions: list[dict[str, Any]], filename: str = "transactions.csv"
) -> None:
    """Save a list of transactions to CSV."""
    path = Path(filename)
    with path.open(mode="w", newline="", encoding="utf-8") as file_obj:
        writer = csv.writer(file_obj)
        writer.writerow(["Date", "Amount", "Category", "Description"])
        for txn in transactions:
            normalized = _normalize_transaction(txn)
            writer.writerow(
                [
                    normalized["date"],
                    normalized["amount"],
                    normalized["category"],
                    normalized["description"],
                ]
            )


def load_transactions_from_csv(filename: str = "transactions.csv") -> list[TransactionRecord]:
    """Load transactions from CSV."""
    path = Path(filename)
    data: list[TransactionRecord] = []
    with path.open(mode="r", newline="", encoding="utf-8") as file_obj:
        reader = csv.DictReader(file_obj)
        for row in reader:
            data.append(
                {
                    "date": row["Date"],
                    "amount": float(row["Amount"]),
                    "category": row["Category"],
                    "description": row["Description"],
                }
            )
    return data


def save_transactions_to_json(
    transactions: list[dict[str, Any]], filename: str = "transactions.json"
) -> None:
    """Save transactions to JSON."""
    path = Path(filename)
    normalized_data = [_normalize_transaction(txn) for txn in transactions]
    with path.open(mode="w", encoding="utf-8") as file_obj:
        json.dump(normalized_data, file_obj, indent=2)


def load_transactions_from_json(filename: str = "transactions.json") -> list[TransactionRecord]:
    """Load transactions from JSON."""
    path = Path(filename)
    with path.open(mode="r", encoding="utf-8") as file_obj:
        data = json.load(file_obj)
    return [_normalize_transaction(txn) for txn in data]


def init_database(db_path: str = "finance.db") -> None:
    """Create the transactions table if missing."""
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                amount REAL,
                category TEXT,
                description TEXT
            )
            """
        )


def add_transaction_to_db(transaction: dict[str, Any], db_path: str = "finance.db") -> None:
    """Insert one transaction into SQLite."""
    txn = _normalize_transaction(transaction)
    with sqlite3.connect(db_path) as conn:
        conn.execute(
            "INSERT INTO transactions (date, amount, category, description) VALUES (?, ?, ?, ?)",
            (txn["date"], txn["amount"], txn["category"], txn["description"]),
        )


def load_transactions_from_db(db_path: str = "finance.db") -> list[TransactionRecord]:
    """Load all transactions from SQLite."""
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT date, amount, category, description FROM transactions ORDER BY date ASC"
        ).fetchall()

    return [
        {
            "date": row[0],
            "amount": float(row[1]),
            "category": row[2],
            "description": row[3],
        }
        for row in rows
    ]
