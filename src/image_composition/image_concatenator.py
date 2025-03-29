from PIL import Image
from math import ceil

class ImageConcatenator:
    def __init__(self, columns: int = 4, max_thumbnail_size: tuple[int, int] = (200, 200)):
        self.columns = columns
        self.max_thumbnail_size = max_thumbnail_size
        self.images = []
        self.border_color = (0, 0, 0)
        self.border_width = 1

    def add_image(self, img: Image.Image):
        thumbnail = self._add_border(self._resize_image(img))
        self.images.append(thumbnail)

    def _resize_image(self, img: Image.Image) -> Image.Image:
        img.thumbnail(self.max_thumbnail_size)
        return img

    def _add_border(self, img: Image.Image) -> Image.Image:
        new_size = (
            img.width + 2 * self.border_width,
            img.height + 2 * self.border_width
        )
        bordered = Image.new("RGB", new_size, self.border_color)
        bordered.paste(img, (self.border_width, self.border_width))
        return bordered

    def concatenate(self) -> Image.Image:
        if not self.images:
            return Image.new("RGB", (1, 1))

        rows = ceil(len(self.images) / self.columns)
        thumb_width, thumb_height = self.images[0].size

        total_width = self.columns * thumb_width
        total_height = rows * thumb_height
        composite = Image.new("RGB", (total_width, total_height))

        for index, img in enumerate(self.images):
            x = (index % self.columns) * thumb_width
            y = (index // self.columns) * thumb_height
            composite.paste(img, (x, y))

        return composite