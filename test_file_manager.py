import unittest
import os
import shutil
from file_ops import detect_duplicates, get_video_titles

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_dir"
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, "test1.mp4"), "w") as f:
            f.write("test")
        with open(os.path.join(self.test_dir, "test1.pdf"), "w") as f:
            f.write("test")
        with open(os.path.join(self.test_dir, "test2.mp4"), "w") as f:
            f.write("test")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_detect_duplicates(self):
        self.assertFalse(detect_duplicates(self.test_dir))
        os.remove(os.path.join(self.test_dir, "test1.pdf"))
        self.assertTrue(detect_duplicates(self.test_dir))

    def test_get_video_titles(self):
        import io
        from contextlib import redirect_stdout
        f = io.StringIO()
        with redirect_stdout(f):
            get_video_titles(self.test_dir)
        output = f.getvalue()
        self.assertIn("test1", output)
        self.assertIn("test2", output)

if __name__ == "__main__":
    unittest.main()
