import unittest
from unittest.mock import patch, mock_open, MagicMock
from pathlib import Path
from src.code_handling.file_system_loader import FileSystemLoader
from src.code_handling.code_file import CodeFile

TEST_DATA_PATH = Path("tests/test_data")


class TestFileSystemLoader(unittest.TestCase):

    @patch("os.walk")
    @patch("pathlib.Path.exists", return_value=True)
    @patch("pathlib.Path.is_dir", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="test content")
    def test_load_code_files(self, mock_file, mock_is_dir, mock_exists, mock_os_walk):
        mock_os_walk.return_value = [
            (str(TEST_DATA_PATH), ["subdir"], ["file1.py", "file2.txt"]),
            (str(TEST_DATA_PATH / "subdir"), [], ["file3.py"])
        ]

        loader = FileSystemLoader()
        result = loader.load_code_files([str(TEST_DATA_PATH)], ["*.py"], ["ignore*"])

        self.assertEqual(len(result), 2)
        self.assertIsInstance(result[0], CodeFile)
        self.assertEqual(result[0].content, "test content")

    @patch("pathlib.Path.is_file", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="file content")
    def test_process_single_file_matching_pattern(self, mock_file, mock_is_file):
        loader = FileSystemLoader()
        result = loader._process_single_file(TEST_DATA_PATH / "test.py", ["*.py"])

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].content, "file content")

    @patch("pathlib.Path.is_file", return_value=True)
    def test_process_single_file_not_matching_pattern(self, mock_is_file):
        loader = FileSystemLoader()
        result = loader._process_single_file(TEST_DATA_PATH / "test.txt", ["*.py"])

        self.assertEqual(result, [])

    def test_is_ignored(self):
        loader = FileSystemLoader()
        self.assertTrue(loader._is_ignored(TEST_DATA_PATH / "ignore_this.py", ["ignore*"]))
        self.assertFalse(loader._is_ignored(TEST_DATA_PATH / "valid.py", ["ignore*"]))

    @patch("builtins.open", new_callable=mock_open, read_data="valid content")
    def test_load_file_content(self, mock_file):
        loader = FileSystemLoader()
        code_file = loader._load_file_content(TEST_DATA_PATH / "test.py")
        self.assertEqual(code_file.content, "valid content")
        self.assertEqual(code_file.filename, str(TEST_DATA_PATH / "test.py"))

    @patch("builtins.open", side_effect=UnicodeDecodeError("codec", b"", 0, 1, "reason"))
    def test_load_file_content_unicode_error(self, mock_file):
        loader = FileSystemLoader()
        code_file = loader._load_file_content(TEST_DATA_PATH / "invalid.py")
        self.assertEqual(code_file.content, "")
        self.assertEqual(code_file.filename, str(TEST_DATA_PATH / "invalid.py"))


if __name__ == "__main__":
    unittest.main()
