import hashlib
import unittest

from PIL import Image

from src.main.python.code_loading.code_file import CodeFile
from src.main.python.image_generation.code_image_generator import CodeImageGenerator


class TestCodeImageGenerator(unittest.TestCase):

    def setUp(self):
        self.test_code = "ttt\n  t x a b\n\n\n\ttest test\nxx"
        self.code_file = CodeFile(self.test_code, "test.java")
        self.generator = CodeImageGenerator(500, 1000, 10)

    def test_image_generation_matches_reference(self):
        expected_reference_hash = "975ae340d0385dc056d1f87c5499720c"
        generated_image = self.generator.generate_image(self.code_file)
        generated_hash = self._calculate_image_hash(generated_image)

        self.assertEqual(
            generated_hash,
            expected_reference_hash,
            "Generated image does not match.\n"
            f"Expected hash: {expected_reference_hash}\n"
            f"Result hash: {generated_hash}\n"
        )

    def _calculate_image_hash(self, image: Image.Image) -> str:
        return hashlib.md5(image.convert('RGB').tobytes()).hexdigest()

if __name__ == "__main__":
    unittest.main()
