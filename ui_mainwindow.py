# ui_mainwindow.py
# Description: Defines the main window UI using PyQt and embeds a chart.

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QFormLayout, QLineEdit, QDateEdit,
    QComboBox, QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QHBoxLayout, QTabWidget
)
from PyQt5.QtCore import QDate
from models import Transaction
from analysis import get_chart_canvas

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Personal Finance Tracker")
        self.setGeometry(100, 100, 900, 700)
        self.transactions = []  # List of Transaction objects
        self.setup_ui()

    def setup_ui(self):
        # Create form inputs
        self.date_input = QDateEdit()
        self.date_input.setDate(QDate.currentDate())
        self.amount_input = QLineEdit()
        self.category_input = QComboBox()
        self.category_input.addItems(["Food", "Rent", "Salary", "Entertainment"])
        self.desc_input = QLineEdit()

        # Create buttons for transaction actions
        self.add_btn = QPushButton("Add Transaction")
        self.edit_btn = QPushButton("Edit Transaction")
        self.del_btn = QPushButton("Delete Transaction")
        self.chart_btn = QPushButton("Update Chart")

        # Connect buttons to functions
        self.add_btn.clicked.connect(self.add_transaction)
        self.edit_btn.clicked.connect(self.edit_transaction)
        self.del_btn.clicked.connect(self.delete_transaction)
        self.chart_btn.clicked.connect(self.update_chart)

        # Create a form layout for inputs
        form_layout = QFormLayout()
        form_layout.addRow("Date:", self.date_input)
        form_layout.addRow("Amount:", self.amount_input)
        form_layout.addRow("Category:", self.category_input)
        form_layout.addRow("Description:", self.desc_input)

        # Layout for buttons
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_btn)
        button_layout.addWidget(self.edit_btn)
        button_layout.addWidget(self.del_btn)
        button_layout.addWidget(self.chart_btn)

        # Table to display transactions
        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["Date", "Amount", "Category", "Description"])

        # Chart area layout
        self.chart_layout = QVBoxLayout()
        # Initially, add a placeholder chart
        self.chart_layout.addWidget(get_chart_canvas([]))

        # Combine form and buttons in one vertical layout
        form_container = QVBoxLayout()
        form_container.addLayout(form_layout)
        form_container.addLayout(button_layout)

        # Use a tab widget to separate transaction entry and chart visualization
        self.tabs = QTabWidget()
        # Tab 1: Transactions
        transaction_tab = QWidget()
        trans_layout = QVBoxLayout()
        trans_layout.addLayout(form_container)
        trans_layout.addWidget(self.table)
        transaction_tab.setLayout(trans_layout)
        # Tab 2: Visualization
        visualization_tab = QWidget()
        visualization_tab.setLayout(self.chart_layout)

        self.tabs.addTab(transaction_tab, "Transactions")
        self.tabs.addTab(visualization_tab, "Charts")

        # Main layout for the window
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)

        # Set the central widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def add_transaction(self):
        # Get data from inputs
        date_str = self.date_input.date().toString("yyyy-MM-dd")
        amount_str = self.amount_input.text()
        category = self.category_input.currentText()
        desc = self.desc_input.text()

        # Validate inputs
        if not amount_str or not desc:
            QMessageBox.warning(self, "Input Error", "Please fill in all fields.")
            return
        try:
            amount = float(amount_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount must be a number.")
            return

        txn = Transaction(date_str, amount, category, desc)
        self.transactions.append(txn)
        self.add_transaction_to_table(txn)
        self.clear_form()
        self.update_chart()  # Refresh chart after adding a new transaction

    def add_transaction_to_table(self, txn):
        row = self.table.rowCount()
        self.table.insertRow(row)
        self.table.setItem(row, 0, QTableWidgetItem(txn.date))
        self.table.setItem(row, 1, QTableWidgetItem(str(txn.amount)))
        self.table.setItem(row, 2, QTableWidgetItem(txn.category))
        self.table.setItem(row, 3, QTableWidgetItem(txn.description))

    def edit_transaction(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a transaction to edit.")
            return

        date_str = self.date_input.date().toString("yyyy-MM-dd")
        amount_str = self.amount_input.text()
        category = self.category_input.currentText()
        desc = self.desc_input.text()

        try:
            amount = float(amount_str)
        except ValueError:
            QMessageBox.warning(self, "Input Error", "Amount must be a number.")
            return

        self.table.setItem(row, 0, QTableWidgetItem(date_str))
        self.table.setItem(row, 1, QTableWidgetItem(amount_str))
        self.table.setItem(row, 2, QTableWidgetItem(category))
        self.table.setItem(row, 3, QTableWidgetItem(desc))
        self.transactions[row] = Transaction(date_str, amount, category, desc)
        self.clear_form()
        self.update_chart()

    def delete_transaction(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Selection Error", "Please select a transaction to delete.")
            return
        self.table.removeRow(row)
        self.transactions.pop(row)
        self.update_chart()

    def clear_form(self):
        self.amount_input.clear()
        self.desc_input.clear()
        self.category_input.setCurrentIndex(0)
        self.date_input.setDate(QDate.currentDate())

    def update_chart(self):
        # Remove any existing chart widgets from the chart layout
        for i in reversed(range(self.chart_layout.count())):
            widget = self.chart_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        # Convert transactions to list of dicts for the chart function
        txn_data = [txn.to_dict() for txn in self.transactions]
        canvas = get_chart_canvas([txn.to_dict() for txn in self.transactions])
        self.chart_layout.addWidget(canvas)
