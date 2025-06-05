import os
import unittest
from main import load_stylesheet

class TestMain(unittest.TestCase):
    def test_load_stylesheet_from_other_directory(self,):
        current = os.getcwd()
        try:
            import tempfile
            with tempfile.TemporaryDirectory() as tempdir:
                os.chdir(tempdir)
                content = load_stylesheet("style.qss")
                self.assertIn("QMainWindow", content)
        finally:
            os.chdir(current)

if __name__ == '__main__':
    unittest.main()
