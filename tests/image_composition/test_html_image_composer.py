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
        composer = HtmlImageComposer(output_directory=self.temp_dir.name)
        self.assertTrue(Path(composer.output_directory).exists())
        self.assertTrue(Path(composer.images_directory).exists())
        self.assertEqual(composer.columns, 10)
        self.assertEqual(composer.thumbnail_size, (500, 1000))

    def test_add_image_with_filename(self):
        composer = HtmlImageComposer(output_directory=self.temp_dir.name)
        composer.add_image(self.sample_image, self.code_file_with_name)

        expected_path = Path(composer.images_directory) / "Test.png"
        self.assertTrue(expected_path.exists())
        self.assertEqual(len(composer.image_paths), 1)
        self.assertEqual(
            composer.image_paths[0][1],
            "src/main/java/Test.java"
        )

    def test_add_image_without_filename(self):
        composer = HtmlImageComposer(output_directory=self.temp_dir.name)
        composer.add_image(self.sample_image, self.code_file_without_name)

        expected_path = Path(composer.images_directory) / "image_0.png"
        self.assertTrue(expected_path.exists())
        self.assertIsNone(composer.image_paths[0][1])

    def test_html_generation(self):
        composer = HtmlImageComposer(
            output_directory=self.temp_dir.name,
            columns=3
        )
        composer.add_image(self.sample_image, self.code_file_with_name)
        composer.generate_html()

        html_file = Path(self.temp_dir.name) / "index.html"
        self.assertTrue(html_file.exists())

        html_content = html_file.read_text()
        self.assertIn('<div class="grid-container">', html_content)
        self.assertIn('Test.png', html_content)
        self.assertIn(
            'data-original-filename="src/main/java/Test.java"',
            html_content
        )

        css_file = Path(self.temp_dir.name) / "styles.css"
        self.assertTrue(css_file.exists())

        css_content = css_file.read_text()
        self.assertIn('grid-template-columns: repeat(3, 1fr)', css_content)

    def test_thumbnail_processing(self):
        composer = HtmlImageComposer(
            output_directory=self.temp_dir.name,
            thumbnail_size=(200, 200)
        )
        composer.add_image(self.sample_image, self.code_file_with_name)

        processed_image = Image.open(Path(composer.images_directory) / "Test.png")
        self.assertLessEqual(processed_image.width, 200 + 1)
        self.assertLessEqual(processed_image.height, 200 + 1)
        self.assertEqual(processed_image.getpixel((0, 0)), (0, 0, 0))

    def test_special_characters_in_filename(self):
        code_file = CodeFile(content="test", filename="src/Test#1.java")
        composer = HtmlImageComposer(output_directory=self.temp_dir.name)
        composer.add_image(self.sample_image, code_file)

        expected_path = Path(composer.images_directory) / "Test#1.png"
        self.assertTrue(expected_path.exists())

    def test_multiple_images(self):
        composer = HtmlImageComposer(
            output_directory=self.temp_dir.name,
            columns=2
        )

        for i in range(5):
            code_file = CodeFile(content="test", filename=f"File{i}.java")
            composer.add_image(self.sample_image, code_file)

        composer.generate_html()

        html_content = (Path(self.temp_dir.name) / "index.html").read_text()
        self.assertEqual(html_content.count('class="grid-item"'), 5)

        css_content = (Path(self.temp_dir.name) / "styles.css").read_text()
        self.assertIn('grid-template-columns: repeat(2, 1fr)', css_content)
        self.assertIn('<link rel="stylesheet" href="styles.css">', html_content)

    def test_empty_composer(self):
        composer = HtmlImageComposer(output_directory=self.temp_dir.name)
        composer.generate_html()

        html_content = (Path(self.temp_dir.name) / "index.html").read_text()
        self.assertIn('<div class="grid-container">', html_content)
        self.assertNotIn('class="grid-item"', html_content)

        # Verify CSS file exists
        css_path = Path(self.temp_dir.name) / "styles.css"
        self.assertTrue(css_path.exists())

    def test_css_structure(self):
        composer = HtmlImageComposer(output_directory=self.temp_dir.name)
        composer.add_image(self.sample_image, self.code_file_with_name)
        composer.generate_html()

        html_content = (Path(self.temp_dir.name) / "index.html").read_text()
        self.assertIn(self.code_file_with_name.filename, html_content)
        self.assertIn('<link rel="stylesheet" href="styles.css">', html_content)

        css_content = (Path(self.temp_dir.name) / "styles.css").read_text()
        self.assertIn('z-index: 2', css_content)
        self.assertIn('font-size: 20px', css_content)
        self.assertIn('transition: opacity 0.3s ease', css_content)


if __name__ == "__main__":
    unittest.main()
