from pathlib import Path
from PIL import Image

from src.code_handling.code_file import CodeFile


class HtmlImageComposer:
    def __init__(self,
                 output_dir: str = "output",
                 columns: int = 10,
                 thumbnail_size: tuple[int, int] = (500, 1000)):
        self.columns = columns
        self.thumbnail_size = thumbnail_size
        self.output_dir = Path(output_dir)
        self.images_dir = self.output_dir / "images"
        self.image_paths = []
        self.border_color = (0, 0, 0)
        self.border_width = 1

        self.images_dir.mkdir(parents=True, exist_ok=True)

    def add_image(self, image: Image.Image, code_file: CodeFile):
        thumbnail = self._process_image(image)

        if code_file.filename:
            filename = f"{Path(code_file.filename).stem}.png"
        else:
            filename = f"image_{len(self.image_paths)}.png"

        save_path = self.images_dir / filename
        thumbnail.save(save_path)
        self.image_paths.append((save_path, code_file.filename))

    def _process_image(self, image: Image.Image) -> Image.Image:
        image.thumbnail(self.thumbnail_size)
        return self._add_border(image)

    def _add_border(self, image: Image.Image) -> Image.Image:
        new_size = (
            image.width + self.border_width,
            image.height + self.border_width
        )
        bordered = Image.new("RGB", new_size, self.border_color)
        bordered.paste(image, (self.border_width, self.border_width))
        return bordered

    def generate_html(self):
        html = []
        html.append('<!DOCTYPE html>\n<html>\n<head>')
        html.append('<style>')
        html.append(f'''
            .grid-container {{
                display: grid;
                grid-template-columns: repeat({self.columns}, 1fr);
                gap: 2px;
                padding: 2px;
            }}
            .grid-item {{
                position: relative;
                border: 1px solid #ddd;
                padding: 2px;
                transition: all 0.3s ease;
            }}
            .filename {{
                position: absolute;
                bottom: 10px;
                left: 10px;
                background: rgba(0,0,0,0.8);
                color: white;
                padding: 5px 10px;
                font-family: Arial;
                font-size: 20px;
                border-radius: 3px;
                opacity: 0;
                transition: opacity 0.3s ease;
                pointer-events: none;
                z-index: 2;  /* Wichtig: Text über Bild */
            }}
            .grid-item:hover .filename {{
                opacity: 1;
            }}
            img {{
                width: 100%;
                height: auto;
                display: block;
                position: relative;  /* Für z-index Kontext */
                z-index: 1;  /* Bild unter Text */
            }}
        ''')
        html.append('</style>\n</head>\n<body>')
        html.append('<div class="grid-container">')

        for image_path, filename in self.image_paths:
            relative_path = image_path.relative_to(self.output_dir)
            display_name = Path(filename).name if filename else "unnamed"
            html.append(f'''
                <div class="grid-item">
                    <img src="{relative_path}" alt="{filename}">
                    <div class="filename" data-original-filename="{filename}">
                        {display_name}
                    </div>
                </div>
            ''')

        html.append('</div>\n</body>\n</html>')

        with open(self.output_dir / 'index.html', 'w') as file:
            file.write('\n'.join(html))

        print(f"HTML generated at: {(self.output_dir / 'index.html').absolute()}")