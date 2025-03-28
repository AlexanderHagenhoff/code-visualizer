from PIL import Image, ImageDraw
from src.code_handling.code_file import CodeFile


class CodeImageGenerator:
    def __init__(
            self,
            image_width: int,
            image_height: int,
            point_size: int = 3,
            background_color: tuple[int, int, int] = (30, 31, 34),
            text_color: tuple[int, int, int] = (188, 190, 196),
            tab_size: int = 5
    ):
        self.image_width = image_width
        self.image_height = image_height
        self.point_size = point_size
        self.background_color = background_color
        self.text_color = text_color
        self.tab_size = tab_size

    def generate_image(self, code_file: CodeFile) -> Image.Image:
        image = Image.new("RGB", (self.image_width, self.image_height), self.background_color)
        draw = ImageDraw.Draw(image)
        lines = code_file.content.splitlines(keepends=True)
        y_offset = 0

        self._draw_lines(draw, lines, y_offset)

        return image

    def _draw_lines(self, draw: ImageDraw.Draw, lines: list[str], y_offset: int):
        for line in lines:
            self._draw_line(draw, line, y_offset)
            y_offset += self.point_size

    def _draw_line(self, draw: ImageDraw.Draw, line: str, y_offset: int):
        x_offset = 0
        for char in line:
            self._draw_char(draw, char, x_offset, y_offset)
            x_offset += self._get_char_offset(char)

    def _draw_char(self, draw: ImageDraw.Draw, char: str, x_offset: int, y_offset: int):
        color = self._get_char_color(char)
        self._draw_point(draw, x_offset, y_offset, color)

    def _get_char_color(self, char: str) -> tuple[int, int, int]:
        if char in (' ', '\t', '\n'):
            return self.background_color

        return self.text_color

    def _draw_point(self, draw: ImageDraw.Draw, x: int, y: int, color: tuple[int, int, int]):
        draw.rectangle([x, y, x + self.point_size, y + self.point_size], fill=color)

    def _get_char_offset(self, char: str) -> int:
        if char == '\t':
            return self.tab_size * self.point_size \

        return self.point_size