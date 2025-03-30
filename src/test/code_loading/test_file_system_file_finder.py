import shutil
import tempfile
import unittest
from pathlib import Path

from src.main.python.code_loading.file_system_file_finder import FileSystemFileFinder


class TestFileSystemFileFinder(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.sub_dir = Path(self.test_dir) / 'sub_dir'
        self.sub_dir.mkdir(parents=True, exist_ok=True)

        self.java_file_1 = Path(self.test_dir) / 'Test1.java'
        self.java_file_2 = Path(self.test_dir) / 'Test2.java'
        self.java_file_3 = self.sub_dir / 'Test3.java'
        self.txt_file = Path(self.test_dir) / 'Test.txt'

        self.java_file_1.touch()
        self.java_file_2.touch()
        self.java_file_3.touch()
        self.txt_file.touch()

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_filter_out_unwanted_files(self):
        file_finder = FileSystemFileFinder(self.test_dir)

        found_files = file_finder.find_files(['*.java'])

        self.assertEqual(len(found_files), 3)
        self.assertIn(self.java_file_1, found_files)
        self.assertIn(self.java_file_2, found_files)
        self.assertIn(self.java_file_3, found_files)
        self.assertNotIn(self.txt_file, found_files)

    def test_find_multiple_files_by_different_patterns(self):
        file_finder = FileSystemFileFinder(self.test_dir)

        found_files = file_finder.find_files(['*.java', '*.txt'])

        self.assertEqual(len(found_files), 4)
        self.assertIn(self.java_file_1, found_files)
        self.assertIn(self.java_file_2, found_files)
        self.assertIn(self.java_file_3, found_files)
        self.assertIn(self.txt_file, found_files)

    def test_empty_directory(self):
        empty_dir = tempfile.mkdtemp()

        file_finder = FileSystemFileFinder(empty_dir)
        java_files = file_finder.find_files(['*.java'])

        self.assertEqual(len(java_files), 0)

        shutil.rmtree(empty_dir)

    def test_empty_file_pattern(self):
        empty_dir = tempfile.mkdtemp()

        file_finder = FileSystemFileFinder(empty_dir)

        with self.assertRaises(ValueError):
            file_finder.find_files([])

        shutil.rmtree(empty_dir)

    def test_non_existent_directory(self):
        non_existent_dir = "non_existent_directory"
        file_finder = FileSystemFileFinder(non_existent_dir)

        with self.assertRaises(FileNotFoundError):
            file_finder.find_files(['*.java'])


if __name__ == '__main__':
    unittest.main()
