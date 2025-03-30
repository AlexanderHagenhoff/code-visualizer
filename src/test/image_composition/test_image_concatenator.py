import unittest
import os
import hashlib
from PIL import Image

from src.main.python.image_composition.image_concatenator import ImageConcatenator


class TestImageConcatenator(unittest.TestCase):
    TEST_DATA_DIR = "resources/concatenator"
    REFERENCE_HASHES = {
        'empty': '693e9af84d3dfcc71e640e005bdc5e2e',
        'single': '8a98d1fb40ab76530092636750085ea4',
        'grid_2x2': 'ed6bd0d60ff692c489113f9351bf37e9'
    }

    def setUp(self):
        os.makedirs(self.TEST_DATA_DIR, exist_ok=True)
        self._create_test_images()

    def _create_test_images(self):
        self.test_images = []

        for file_index in range(0, 4):
            image_path = f"{self.TEST_DATA_DIR}/test_{file_index}.png"
            self.test_images.append(Image.open(image_path))

    def tearDown(self):
        for test_file in self.test_images:
            test_file.close()

    def _calculate_image_hash(self, image: Image.Image) -> str:
        return hashlib.md5(image.tobytes()).hexdigest()

    def test_empty_concatenation(self):
        concatenator = ImageConcatenator()
        result = concatenator.concatenate()
        self.assertEqual(self._calculate_image_hash(result), self.REFERENCE_HASHES['empty'])

    def test_single_image(self):
        concatenator = ImageConcatenator(columns=1, max_thumbnail_size=(10, 10))
        concatenator.add_image(self.test_images[0])
        result = concatenator.concatenate()
        self.assertEqual(self._calculate_image_hash(result), self.REFERENCE_HASHES['single'])

    def test_grid_layout(self):
        concatenator = ImageConcatenator(columns=2, max_thumbnail_size=(10, 10))
        for img in self.test_images:
            concatenator.add_image(img)
        result = concatenator.concatenate()
        self.assertEqual(self._calculate_image_hash(result), self.REFERENCE_HASHES['grid_2x2'])

    def test_border(self):
        concatenator = ImageConcatenator()
        original_img = self.test_images[0]
        concatenator.add_image(original_img)

        bordered_img = concatenator.images[0]
        self.assertEqual(bordered_img.width, original_img.width + 2)
        self.assertEqual(bordered_img.height, original_img.height + 2)

        self.assertEqual(bordered_img.getpixel((0, 0)), (0, 0, 0))
        self.assertEqual(bordered_img.getpixel((1, 1)), original_img.getpixel((0, 0)))

    def test_image_resizing(self):
        concatenator = ImageConcatenator(max_thumbnail_size=(10, 10))
        large_img = Image.new('RGB', (100, 100), (255, 255, 255))
        concatenator.add_image(large_img)

        resized_img = concatenator.images[0]
        self.assertLessEqual(resized_img.width, 12)
        self.assertLessEqual(resized_img.height, 12)
        self.assertEqual(resized_img.size, (12, 12))


if __name__ == '__main__':
    unittest.main()
