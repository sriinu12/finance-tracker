# Finance Tracker

Desktop personal finance tracker built with Python and PyQt5.

## What is improved
- Stronger data model using a typed `Transaction` dataclass with validation.
- Safer storage layer with normalized CSV/JSON/SQLite handling and UTF-8 support.
- Upgraded analytics chart with cleaner monthly trends and polished visuals.
- Refreshed trendy UI:
  - Summary metric cards (balance, income, expense, transaction count)
  - Search + category filters
  - Row selection auto-fills the edit form
  - Autosave on every change and on app close
- Better startup resiliency when stylesheet is missing or unreadable.

## Features
- Add, edit, and delete transactions
- Live chart for monthly income vs expense
- Filter transactions by text and category
- Save/load transaction history (JSON)
- CSV/JSON/SQLite storage helpers for data portability

## Requirements
- Python 3.13+
- PyQt5
- pandas
- matplotlib
- seaborn

## Installation
1. Clone the repository:
   ```sh
   git clone https://github.com/username/finance-tracker.git
   cd finance-tracker
   ```
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Run the application:
   ```sh
   python main.py
   ```

## Tests
```sh
python -m unittest discover -s tests -v
```
