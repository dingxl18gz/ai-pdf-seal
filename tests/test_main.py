import os
import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestMainFunctions(unittest.TestCase):
    def test_is_already_sealed_exists(self):
        from main import is_already_sealed
        with patch('main.os.path.exists', return_value=True):
            result = is_already_sealed("test.pdf")
            self.assertTrue(result)

    def test_is_already_sealed_not_exists(self):
        from main import is_already_sealed
        with patch('main.os.path.exists', return_value=False):
            result = is_already_sealed("test.pdf")
            self.assertFalse(result)

    def test_scan_directory(self):
        from main import scan_directory
        with patch('main.os.listdir') as mock_listdir:
            mock_listdir.return_value = ["file1.pdf", "file2.pdf", "image.png"]
            result = scan_directory("test_dir")
            self.assertEqual(len(result), 2)
            self.assertTrue(any("file1.pdf" in f for f in result))
            self.assertTrue(any("file2.pdf" in f for f in result))

    def test_scan_directory_excludes_sealed(self):
        from main import scan_directory
        with patch('main.os.listdir') as mock_listdir:
            mock_listdir.return_value = ["file1.pdf", "file1_sealed.pdf", "other.pdf"]
            result = scan_directory("test_dir")
            self.assertEqual(len(result), 2)
            self.assertTrue(any("file1.pdf" in f for f in result))
            self.assertTrue(any("other.pdf" in f for f in result))
            self.assertFalse(any("file1_sealed.pdf" in f for f in result))

    def test_merge_args_with_config(self):
        from main import merge_args_with_config
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('--pdf', default=None)
        parser.add_argument('--image', default=None)
        parser.add_argument('--width', type=int, default=None)
        args = parser.parse_args([])

        config = {'pdf': 'test.pdf', 'image': 'stamp.png', 'width': 100}
        result = merge_args_with_config(args, config)

        self.assertEqual(result.pdf, 'test.pdf')
        self.assertEqual(result.image, 'stamp.png')
        self.assertEqual(result.width, 100)

    def test_merge_args_cli_overrides_config(self):
        from main import merge_args_with_config
        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument('--pdf', default=None)
        args = parser.parse_args(['--pdf', 'cli_test.pdf'])

        config = {'pdf': 'config_test.pdf'}
        result = merge_args_with_config(args, config)

        self.assertEqual(result.pdf, 'cli_test.pdf')


class TestLoadConfig(unittest.TestCase):
    def test_load_config_exists(self):
        from main import load_config
        import tempfile

        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write("image: stamp.png\nwidth: 50\n")
            temp_path = f.name

        try:
            config = load_config(temp_path)
            self.assertEqual(config['image'], 'stamp.png')
            self.assertEqual(config['width'], 50)
        finally:
            os.remove(temp_path)

    def test_load_config_not_exists(self):
        from main import load_config
        config = load_config('not_exist_config.yaml')
        self.assertEqual(config, {})


if __name__ == "__main__":
    unittest.main()
