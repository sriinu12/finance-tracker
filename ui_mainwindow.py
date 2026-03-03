from __future__ import annotations

from pathlib import Path

from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import (
    QAbstractItemView,
    QComboBox,
    QDateEdit,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QVBoxLayout,
    QWidget,
    QHeaderView,
)

from analysis import get_chart_canvas
from models import Transaction
from storage import load_transactions_from_json, save_transactions_to_json


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.setGeometry(100, 100, 1080, 760)

        self.data_file = Path(__file__).with_name("transactions.json")
        self.transactions: list[Transaction] = []

        self.setup_ui()
        self.load_transactions(silent=True)

    def setup_ui(self) -> None:
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.date_input.setCalendarPopup(True)

        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Use positive for income, negative for expense")

        self.category_input = QComboBox()
        self.category_input.addItems(
            ["Food", "Rent", "Salary", "Entertainment", "Utilities", "Travel", "Health", "Other"]
        )

        self.desc_input = QLineEdit()
        self.desc_input.setPlaceholderText("Add a short description")

        self.add_btn = QPushButton("Add")
        self.edit_btn = QPushButton("Update")
        self.del_btn = QPushButton("Delete")
        self.chart_btn = QPushButton("Refresh Chart")
        self.save_btn = QPushButton("Save")
        self.load_btn = QPushButton("Reload")

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search descriptions and categories")
        self.filter_category = QComboBox()
        self.filter_category.addItems(["All Categories"] + [self.category_input.itemText(i) for i in range(self.category_input.count())])

        self.add_btn.clicked.connect(self.add_transaction)
        self.edit_btn.clicked.connect(self.edit_transaction)
        self.del_btn.clicked.connect(self.delete_transaction)
        self.chart_btn.clicked.connect(self.update_chart)
        self.save_btn.clicked.connect(self.save_transactions)
        self.load_btn.clicked.connect(self.load_transactions)
        self.search_input.textChanged.connect(self.apply_filters)
        self.filter_category.currentTextChanged.connect(self.apply_filters)

        form_layout = QFormLayout()
        form_layout.addRow("Date", self.date_input)
        form_layout.addRow("Amount", self.amount_input)
        form_layout.addRow("Category", self.category_input)
        form_layout.addRow("Description", self.desc_input)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.del_btn)
        button_layout.addWidget(self.chart_btn)
        button_layout.addWidget(self.save_btn)
        button_layout.addWidget(self.load_btn)

        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Search"))
        filter_layout.addWidget(self.search_input)
        filter_layout.addWidget(QLabel("Category"))
        filter_layout.addWidget(self.filter_category)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Date", "Amount", "Category", "Description"])
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.table.itemSelectionChanged.connect(self.populate_form_from_selection)

        self.chart_layout = QVBoxLayout()
        self.chart_layout.addWidget(get_chart_canvas([]))

        balance_card, self.balance_label = self._create_metric_card("Balance", "0.00")
        income_card, self.income_label = self._create_metric_card("Income", "0.00")
        expense_card, self.expense_label = self._create_metric_card("Expense", "0.00")
        count_card, self.count_label = self._create_metric_card("Transactions", "0")

        metric_row = QHBoxLayout()
        metric_row.addWidget(balance_card)
        metric_row.addWidget(income_card)
        metric_row.addWidget(expense_card)
        metric_row.addWidget(count_card)

        transaction_tab = QWidget()
        trans_layout = QVBoxLayout()
        trans_layout.addLayout(form_layout)
        trans_layout.addLayout(button_layout)
        trans_layout.addLayout(filter_layout)
        trans_layout.addWidget(self.table)
        transaction_tab.setLayout(trans_layout)

        visualization_tab = QWidget()
        visualization_tab.setLayout(self.chart_layout)

        self.tabs = QTabWidget()
        self.tabs.addTab(transaction_tab, "Transactions")
        self.tabs.addTab(visualization_tab, "Charts")

        main_layout = QVBoxLayout()
        main_layout.addLayout(metric_row)
        main_layout.addWidget(self.tabs)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def _create_metric_card(self, title: str, value: str) -> tuple[QFrame, QLabel]:
        card = QFrame()
        card.setObjectName("metricCard")
        layout = QVBoxLayout(card)

        title_label = QLabel(title)
        title_label.setObjectName("metricTitle")
        value_label = QLabel(value)
        value_label.setObjectName("metricValue")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card, value_label

    def _collect_form_input(self) -> Transaction | None:
        date_str = self.date_input.date().toString("yyyy-MM-dd")
        amount_str = self.amount_input.text().strip()
        category = self.category_input.currentText()
        desc = self.desc_input.text().strip()

        if not amount_str or not desc:
            QMessageBox.warning(self, "Input Error", "Amount and description are required.")
            return None

        try:
            amount = float(amount_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount must be a valid number.")
            return None

        try:
            return Transaction(date=date_str, amount=amount, category=category, description=desc)
        except ValueError as err:
            QMessageBox.warning(self, "Input Error", str(err))
            return None

    def add_transaction(self) -> None:
        txn = self._collect_form_input()
        if not txn:
            return

        self.transactions.append(txn)
        self.add_transaction_to_table(txn)
        self.clear_form()
        self.apply_filters()
        self.update_summary_cards()
        self.update_chart()
        self.save_transactions(silent=True)

    def add_transaction_to_table(self, txn: Transaction) -> None:
        row = self.table.rowCount()
        self.table.insertRow(row)
        self._set_table_row(row, txn)

    def _set_table_row(self, row: int, txn: Transaction) -> None:
        self.table.setItem(row, 0, QTableWidgetItem(txn.date))
        self.table.setItem(row, 1, QTableWidgetItem(f"{txn.amount:.2f}"))
        self.table.setItem(row, 2, QTableWidgetItem(txn.category))
        self.table.setItem(row, 3, QTableWidgetItem(txn.description))

    def edit_transaction(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Select a transaction to update.")
            return

        txn = self._collect_form_input()
        if not txn:
            return

        self.transactions[row] = txn
        self._set_table_row(row, txn)
        self.clear_form()
        self.apply_filters()
        self.update_summary_cards()
        self.update_chart()
        self.save_transactions(silent=True)

    def delete_transaction(self) -> None:
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Select a transaction to delete.")
            return

        self.table.removeRow(row)
        self.transactions.pop(row)
        self.clear_form()
        self.apply_filters()
        self.update_summary_cards()
        self.update_chart()
        self.save_transactions(silent=True)

    def populate_form_from_selection(self) -> None:
        row = self.table.currentRow()
        if row < 0 or row >= len(self.transactions):
            return

        txn = self.transactions[row]
        self.date_input.setDate(QDate.fromString(txn.date, "yyyy-MM-dd"))
        self.amount_input.setText(f"{txn.amount:.2f}")
        category_index = self.category_input.findText(txn.category, Qt.MatchFixedString)
        if category_index >= 0:
            self.category_input.setCurrentIndex(category_index)
        self.desc_input.setText(txn.description)

    def clear_form(self) -> None:
        self.amount_input.clear()
        self.desc_input.clear()
        self.category_input.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())
        self.table.clearSelection()

    def apply_filters(self) -> None:
        search_text = self.search_input.text().strip().lower()
        selected_category = self.filter_category.currentText()

        for row, txn in enumerate(self.transactions):
            matches_text = (
                search_text in txn.description.lower() or search_text in txn.category.lower() or search_text in txn.date
            )
            matches_category = selected_category == "All Categories" or txn.category == selected_category
            self.table.setRowHidden(row, not (matches_text and matches_category))

    def update_summary_cards(self) -> None:
        total_income = sum(txn.amount for txn in self.transactions if txn.amount > 0)
        total_expense = sum(-txn.amount for txn in self.transactions if txn.amount < 0)
        balance = total_income - total_expense

        self.balance_label.setText(f"{balance:,.2f}")
        self.income_label.setText(f"{total_income:,.2f}")
        self.expense_label.setText(f"{total_expense:,.2f}")
        self.count_label.setText(str(len(self.transactions)))

    def update_chart(self) -> None:
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        txn_data = [txn.to_dict() for txn in self.transactions]
        self.chart_layout.addWidget(get_chart_canvas(txn_data))

    def save_transactions(self, silent: bool = False) -> None:
        try:
            save_transactions_to_json([txn.to_dict() for txn in self.transactions], str(self.data_file))
        except OSError as err:
            QMessageBox.critical(self, "Save Error", f"Failed to save transactions: {err}")
            return

        if not silent:
            QMessageBox.information(self, "Saved", f"Data saved to {self.data_file.name}")

    def load_transactions(self, silent: bool = False) -> None:
        if not self.data_file.exists():
            self.transactions = []
            self.table.setRowCount(0)
            self.update_summary_cards()
            self.update_chart()
            return

        try:
            data = load_transactions_from_json(str(self.data_file))
            self.transactions = [Transaction.from_dict(item) for item in data]
        except (OSError, ValueError, KeyError) as err:
            QMessageBox.critical(self, "Load Error", f"Failed to load transactions: {err}")
            return

        self.table.setRowCount(0)
        for txn in self.transactions:
            self.add_transaction_to_table(txn)

        self.apply_filters()
        self.update_summary_cards()
        self.update_chart()

        if not silent:
            QMessageBox.information(self, "Loaded", f"Loaded {len(self.transactions)} transactions")

    def closeEvent(self, event: QCloseEvent) -> None:
        self.save_transactions(silent=True)
        event.accept()
