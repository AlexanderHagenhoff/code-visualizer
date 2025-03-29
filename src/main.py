from image_composition.html_image_composer import HtmlImageComposer
from image_generation.code_image_generator import CodeImageGenerator
from src.code_handling.file_system_loader import FileSystemLoader

def sort_images_by_height(images_with_files):
    decorated = [(image.height, image, file) for image, file in images_with_files]
    decorated.sort(reverse=True, key=lambda x: x[0])
    return [(image, file) for height, image, file in decorated]

if __name__ == "__main__":
    #directory = r'D:\dev\spring-boot\spring-boot-project\spring-boot-actuator'
    directory = r'D:/Python/dev/code-visualizer'

    loader = FileSystemLoader()
    ignore_patterns = [
        "**/__pycache__/**",
        "**/venv/**"
    ]

    found_files = loader.load_code_files([directory], ["*.py"], ignore_patterns=ignore_patterns)

    generator = CodeImageGenerator(400, 300, 3, 5)

    images_with_files = []
    for file in found_files:
        image = generator.generate_image(file)
        images_with_files.append((image, file))

    sorted_images = sort_images_by_height(images_with_files)

    composer = HtmlImageComposer(
        output_directory="../output/html_output",
        columns=20,
        thumbnail_size=(500, 1000)
    )

    for image, file in sorted_images:
        composer.add_image(image, file)

    composer.generate_html()