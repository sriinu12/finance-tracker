# main.py
# Description: Launches the PyQt application for the Personal Finance Tracker.

import sys
import os
from PyQt5.QtWidgets import QApplication
from ui_mainwindow import MainWindow

def load_stylesheet(file_path):
    """Load QSS stylesheet from a file path relative to this module."""
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    with open(abs_path, "r") as file:
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