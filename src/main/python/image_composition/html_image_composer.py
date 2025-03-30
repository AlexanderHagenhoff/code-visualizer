from pathlib import Path

from PIL import Image

from src.main.python.code_handling.code_file import CodeFile


class HtmlImageComposer:
    IMAGES_DIRECTORY_NAME = "images"
    TEMPLATES_DIRECTORY_NAME = "../../resources/templates"
    DEFAULT_OUTPUT_DIRECTORY_NAME = "output"
    STYLESHEET_FILENAME = "styles.css"
    BASE_TEMPLATE_FILENAME = "base.html"
    OUTPUT_HTML_FILENAME = "index.html"
    IMAGE_FILE_EXTENSION = ".png"
    UNNAMED_FILE_PREFIX = "image_"
    UNNAMED_FILE_DISPLAY_NAME = "unnamed"

    COLUMNS_PLACEHOLDER = "{{ columns }}"
    GRID_ITEMS_PLACEHOLDER = "{{ grid_items }}"

    BORDER_COLOR = (0, 0, 0)
    BORDER_WIDTH = 1

    def __init__(
            self,
            output_directory: str = DEFAULT_OUTPUT_DIRECTORY_NAME,
            columns: int = 10,
            thumbnail_size: tuple[int, int] = (500, 1000)
    ):
        self.columns = columns
        self.thumbnail_size = thumbnail_size
        self.output_directory = Path(output_directory)
        self.images_directory = self.output_directory / self.IMAGES_DIRECTORY_NAME
        self.template_directory = Path(__file__).parent / self.TEMPLATES_DIRECTORY_NAME

        self.image_paths = []

        self.images_directory.mkdir(parents=True, exist_ok=True)

    def add_image(self, image: Image.Image, code_file: CodeFile):
        processed_image = self._process_image(image)
        filename = self._generate_filename(code_file)
        save_path = self.images_directory / filename
        processed_image.save(save_path)
        self.image_paths.append((save_path, code_file.filename))

    def _generate_filename(self, code_file: CodeFile) -> str:
        if code_file.filename:
            return f"{Path(code_file.filename).stem}{self.IMAGE_FILE_EXTENSION}"
        return f"{self.UNNAMED_FILE_PREFIX}{len(self.image_paths)}{self.IMAGE_FILE_EXTENSION}"

    def _process_image(self, image: Image.Image) -> Image.Image:
        image.thumbnail(self.thumbnail_size)
        return self._add_border(image)

    def _add_border(self, image: Image.Image) -> Image.Image:
        new_width = image.width + self.BORDER_WIDTH
        new_height = image.height + self.BORDER_WIDTH
        bordered_image = Image.new("RGB", (new_width, new_height), self.BORDER_COLOR)
        bordered_image.paste(image, (self.BORDER_WIDTH, self.BORDER_WIDTH))
        return bordered_image

    def generate_html(self):
        self._copy_stylesheet()
        self._render_html_page()

    def _copy_stylesheet(self):
        stylesheet_template_path = self.template_directory / self.STYLESHEET_FILENAME
        stylesheet_content = stylesheet_template_path.read_text()
        processed_stylesheet = stylesheet_content.replace(
            self.COLUMNS_PLACEHOLDER,
            str(self.columns)
        )
        output_stylesheet_path = self.output_directory / self.STYLESHEET_FILENAME
        output_stylesheet_path.write_text(processed_stylesheet)

    def _render_html_page(self):
        template_path = self.template_directory / self.BASE_TEMPLATE_FILENAME
        html_template = template_path.read_text()
        grid_items = self._generate_grid_items()
        final_html = html_template.replace(
            self.GRID_ITEMS_PLACEHOLDER,
            "\n".join(grid_items)
        )

        output_html_path = self.output_directory / self.OUTPUT_HTML_FILENAME
        output_html_path.write_text(final_html)
        print(f"HTML generated at: {output_html_path.absolute()}")

    def _generate_grid_items(self) -> list[str]:
        return [
            self._create_grid_item(image_path, filename)
            for image_path, filename in self.image_paths
        ]

    def _create_grid_item(self, image_path: Path, filename: str) -> str:
        relative_image_path = image_path.relative_to(self.output_directory)
        display_name = Path(filename).name if filename else self.UNNAMED_FILE_DISPLAY_NAME
        return f'''
            <div class="grid-item">
                <img src="{relative_image_path}" alt="{filename}">
                <div class="filename" data-original-filename="{filename}">
                    {display_name}
                </div>
            </div>
        '''
