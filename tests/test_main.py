import os
import tempfile
import unittest

from main import load_stylesheet


class TestMain(unittest.TestCase):
    def test_load_stylesheet_from_other_directory(self) -> None:
        current = os.getcwd()
        tempdir = tempfile.mkdtemp()
        try:
            os.chdir(tempdir)
            content = load_stylesheet("style.qss")
        finally:
            os.chdir(current)
            os.rmdir(tempdir)

        self.assertIn("QMainWindow", content)

    def test_missing_stylesheet_returns_empty_string(self) -> None:
        self.assertEqual(load_stylesheet("does-not-exist.qss"), "")


if __name__ == "__main__":
    unittest.main()
