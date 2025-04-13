# main.py
# Description: Launches the PyQt application for the Personal Finance Tracker.

import sys
from PyQt5.QtWidgets import QApplication
from ui_mainwindow import MainWindow

def load_stylesheet(file_path):
    """Load QSS stylesheet from a file."""
    with open(file_path, "r") as file:
        return file.read()

def main():
    app = QApplication(sys.argv)
    
    # Load and apply the stylesheet
    stylesheet = load_stylesheet("style.qss")
    app.setStyleSheet(stylesheet)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()