from PIL import Image, ImageDraw


class CodeImageGenerator:
    POINT_SIZE = 2
    BACKGROUND_COLOR = (30, 31, 34)
    TEXT_COLOR = (188, 190, 196)

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

        for line in lines:
            x_offset = 0
            for char in line:
                self.draw_point(x_offset, y_offset, self.TEXT_COLOR)
                x_offset += self.POINT_SIZE

            y_offset += self.POINT_SIZE

    def draw_point(self, x, y, color):
        self.draw.rectangle([x, y, x + self.POINT_SIZE, y + self.POINT_SIZE], fill=color)

    def save_image(self, output_path):
        self.image.save(output_path)
