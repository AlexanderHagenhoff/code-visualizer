from PIL import Image, ImageDraw

class CodeImageGenerator:
    POINT_SIZE = 3
    BACKGROUND_COLOR = (30, 31, 34)
    TEXT_COLOR = (188, 190, 196)
    TAB_SIZE = 3

    def __init__(self, file_path, image_width, image_height):
        self.file_path = file_path
        self.image_width = image_width
        self.image_height = image_height
        self.image = Image.new("RGB", (image_width, image_height), self.BACKGROUND_COLOR)
        self.draw = ImageDraw.Draw(self.image)

    def generate_image(self):
        with open(self.file_path, "r") as file:
            lines = file.readlines()

        y_offset = 0

        self.draw_lines(lines, y_offset)

    def draw_lines(self, lines, y_offset):
        for line in lines:
            self.draw_single_line(line, y_offset)
            y_offset += self.POINT_SIZE

    def draw_single_line(self, line, y_offset):
        x_offset = 0
        for char in line:
            color = self.get_draw_color(char)
            self.draw_point(x_offset, y_offset, color)

            offset = self.get_offset_for_char(char)
            x_offset += offset

    def get_draw_color(self, char):
        if char == " " or char == "\t":
            return self.BACKGROUND_COLOR

        return self.TEXT_COLOR

    def draw_point(self, x, y, color):
        self.draw.rectangle([x, y, x + self.POINT_SIZE, y + self.POINT_SIZE], fill=color)

    def draw_tabs(self, x, y):
        for _ in range(self.TAB_SIZE):
            self.draw_point(x, y, self.BACKGROUND_COLOR)
            x += self.POINT_SIZE

    def get_offset_for_char(self, char):
        if char == "\t":
            return self.TAB_SIZE * self.POINT_SIZE
        else:
            return self.POINT_SIZE

    def save_image(self, output_path):
        self.image.save(output_path)
