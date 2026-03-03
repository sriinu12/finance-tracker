from __future__ import annotations

import os
import sys

from PyQt5.QtWidgets import QApplication

from ui_mainwindow import MainWindow


def load_stylesheet(file_path: str) -> str:
    """Load QSS stylesheet from a file path relative to this module."""
    abs_path = os.path.join(os.path.dirname(__file__), file_path)
    try:
        with open(abs_path, "r", encoding="utf-8") as file_obj:
            return file_obj.read()
    except OSError:
        return ""


def main() -> None:
    app = QApplication(sys.argv)
    stylesheet = load_stylesheet("style.qss")
    if stylesheet:
        app.setStyleSheet(stylesheet)

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
