from PIL import Image, ImageDraw
from src.code_handling.code_file import CodeFile


class CodeImageGenerator:
    def __init__(
            self,
            image_min_width: int = 100,
            image_min_height: int = 100,
            point_width: int = 3,
            point_height: int = 3,
            background_color: tuple[int, int, int] = (30, 31, 34),
            text_color: tuple[int, int, int] = (188, 190, 196),
            tab_size: int = 5
    ):
        self.image_min_width = image_min_width
        self.image_min_height = image_min_height
        self.point_width = point_width
        self.point_height = point_height
        self.background_color = background_color
        self.text_color = text_color
        self.tab_size = tab_size

    def generate_image(self, code_file: CodeFile) -> Image.Image:
        content_width, content_height = self._calculate_content_size(code_file.content)

        image_width = max(self.image_min_width, content_width)
        image_height = max(self.image_min_height, content_height)

        image = Image.new("RGB", (image_width, image_height), self.background_color)
        draw = ImageDraw.Draw(image)

        if code_file.content:
            self._draw_content(draw, code_file.content)

        return image

    def _calculate_content_size(self, content: str) -> tuple[int, int]:
        if not content:
            return (0, 0)

        lines = content.splitlines(keepends=True)
        max_line_width = 0

        for line in lines:
            line_width = 0
            for char in line:
                line_width += self._get_char_offset(char)
            max_line_width = max(max_line_width, line_width)

        total_height = len(lines) * self.point_height

        return (max_line_width, total_height)

    def _draw_content(self, draw: ImageDraw.Draw, content: str):
        lines = content.splitlines(keepends=True)
        y_offset = 0

        for line in lines:
            x_offset = 0
            for char in line:
                self._draw_char(draw, char, x_offset, y_offset)
                x_offset += self._get_char_offset(char)
            y_offset += self.point_height

    def _draw_char(self, draw: ImageDraw.Draw, char: str, x: int, y: int):
        color = self.text_color
        if char in (' ', '\t', '\n'):
            color = self.background_color
        self._draw_point(draw, x, y, color)

    def _draw_point(self, draw: ImageDraw.Draw, x: int, y: int, color: tuple[int, int, int]):
        draw.rectangle([x, y, x + self.point_width, y + self.point_height], fill=color)

    def _get_char_offset(self, char: str) -> int:
        return self.tab_size * self.point_width if char == '\t' else self.point_width