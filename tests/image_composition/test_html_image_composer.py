import tempfile
import unittest
from pathlib import Path

from PIL import Image

from src.code_handling.code_file import CodeFile
from src.image_composition.html_image_composer import HtmlImageComposer


class TestHtmlImageComposer(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.sample_image = Image.new('RGB', (800, 600), (255, 0, 0))
        self.code_file_with_name = CodeFile(
            content="test",
            filename="src/main/java/Test.java"
        )
        self.code_file_without_name = CodeFile(content="test")

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_initialization(self):
        composer = HtmlImageComposer(output_dir=self.temp_dir.name)
        self.assertTrue(Path(composer.output_dir).exists())
        self.assertTrue(Path(composer.images_dir).exists())
        self.assertEqual(composer.columns, 10)
        self.assertEqual(composer.thumbnail_size, (500, 1000))

    def test_add_image_with_filename(self):
        composer = HtmlImageComposer(output_dir=self.temp_dir.name)
        composer.add_image(self.sample_image, self.code_file_with_name)

        expected_path = Path(composer.images_dir) / "Test.png"
        self.assertTrue(expected_path.exists())
        self.assertEqual(len(composer.image_paths), 1)
        self.assertEqual(
            composer.image_paths[0][1],
            "src/main/java/Test.java"
        )

    def test_add_image_without_filename(self):
        composer = HtmlImageComposer(output_dir=self.temp_dir.name)
        composer.add_image(self.sample_image, self.code_file_without_name)

        expected_path = Path(composer.images_dir) / "image_0.png"
        self.assertTrue(expected_path.exists())
        self.assertIsNone(composer.image_paths[0][1])

    def test_html_generation(self):
        composer = HtmlImageComposer(
            output_dir=self.temp_dir.name,
            columns=3
        )
        composer.add_image(self.sample_image, self.code_file_with_name)
        composer.generate_html()

        html_file = Path(self.temp_dir.name) / "index.html"
        self.assertTrue(html_file.exists())

        html_content = html_file.read_text()
        self.assertIn('<div class="grid-container">', html_content)
        self.assertIn('grid-template-columns: repeat(3, 1fr)', html_content)
        self.assertIn('Test.png', html_content)
        self.assertIn(
            'data-original-filename="src/main/java/Test.java"',
            html_content
        )

    def test_thumbnail_processing(self):
        composer = HtmlImageComposer(
            output_dir=self.temp_dir.name,
            thumbnail_size=(200, 200)
        )
        composer.add_image(self.sample_image, self.code_file_with_name)

        processed_image = Image.open(Path(composer.images_dir) / "Test.png")
        self.assertLessEqual(processed_image.width, 200 + 1)
        self.assertLessEqual(processed_image.height, 200 + 1)
        self.assertEqual(processed_image.getpixel((0, 0)), (0, 0, 0))

    def test_special_characters_in_filename(self):
        code_file = CodeFile(content="test", filename="src/Test#1.java")
        composer = HtmlImageComposer(output_dir=self.temp_dir.name)
        composer.add_image(self.sample_image, code_file)

        expected_path = Path(composer.images_dir) / "Test#1.png"
        self.assertTrue(expected_path.exists())

    def test_multiple_images(self):
        composer = HtmlImageComposer(
            output_dir=self.temp_dir.name,
            columns=2
        )

        for i in range(5):
            code_file = CodeFile(content="test", filename=f"File{i}.java")
            composer.add_image(self.sample_image, code_file)

        composer.generate_html()

        html_content = (Path(self.temp_dir.name) / "index.html").read_text()
        self.assertEqual(html_content.count('class="grid-item"'), 5)
        self.assertIn('grid-template-columns: repeat(2, 1fr)', html_content)

    def test_empty_composer(self):
        composer = HtmlImageComposer(output_dir=self.temp_dir.name)
        composer.generate_html()

        html_content = (Path(self.temp_dir.name) / "index.html").read_text()
        self.assertIn('<div class="grid-container">', html_content)
        self.assertNotIn('class="grid-item"', html_content)

    def test_css_structure(self):
        composer = HtmlImageComposer(output_dir=self.temp_dir.name)
        composer.add_image(self.sample_image, self.code_file_with_name)
        composer.generate_html()

        html_content = (Path(self.temp_dir.name) / "index.html").read_text()
        self.assertIn('.filename', html_content)
        self.assertIn('z-index: 2', html_content)
        self.assertIn('transition: opacity 0.3s ease', html_content)
        self.assertIn('font-size: 20px', html_content)


if __name__ == "__main__":
    unittest.main()
