# storage.py
# Description: Provides functions for saving and loading transactions using CSV, JSON, and SQLite.

import csv
import json
import sqlite3

# CSV functions
def save_transactions_to_csv(transactions, filename="transactions.csv"):
    """Save a list of transaction dictionaries to a CSV file."""
    with open(filename, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Date", "Amount", "Category", "Description"])
        for txn in transactions:
            writer.writerow([txn['date'], txn['amount'], txn['category'], txn['description']])

def load_transactions_from_csv(filename="transactions.csv"):
    """Load transactions from a CSV file and return a list of dictionaries."""
    data = []
    with open(filename, mode='r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            txn = {
                'date': row['Date'],
                'amount': float(row['Amount']),
                'category': row['Category'],
                'description': row['Description']
            }
            data.append(txn)
    return data

# JSON functions
def save_transactions_to_json(transactions, filename="transactions.json"):
    """Save transactions (list of dictionaries) to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(transactions, f, indent=4)

def load_transactions_from_json(filename="transactions.json"):
    """Load transactions from a JSON file and return a list of dictionaries."""
    with open(filename, 'r') as f:
        return json.load(f)

# SQLite functions
def init_database(db_path="finance.db"):
    """Initialize the SQLite database and create the transactions table if it doesn't exist."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            amount REAL,
            category TEXT,
            description TEXT
        )
    """)
    conn.commit()
    conn.close()

def add_transaction_to_db(transaction, db_path="finance.db"):
    """
    Add a transaction (dictionary) to the SQLite database.
    transaction: dict with keys 'date', 'amount', 'category', 'description'.
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO transactions (date, amount, category, description) VALUES (?, ?, ?, ?)",
        (transaction['date'], transaction['amount'], transaction['category'], transaction['description'])
    )
    conn.commit()
    conn.close()

def load_transactions_from_db(db_path="finance.db"):
    """Load all transactions from the SQLite database and return a list of dictionaries."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT date, amount, category, description FROM transactions")
    rows = cursor.fetchall()
    conn.close()
    transactions = []
    for row in rows:
        transactions.append({
            'date': row[0],
            'amount': row[1],
            'category': row[2],
            'description': row[3]
        })
    return transactions
