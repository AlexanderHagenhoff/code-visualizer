from image_composition.html_image_composer import HtmlImageComposer
from image_generation.code_image_generator import CodeImageGenerator
from src.code_handling.file_system_loader import FileSystemLoader

if __name__ == "__main__":
    directory = r'D:\dev\spring-boot\spring-boot-project\spring-boot-actuator'

    urls = [
        "https://github.com/AlexanderHagenhoff/spring-boot-postgres-archetype"
    ]

    output_image_path = "output_image.png"

    loader = FileSystemLoader()
    found_files = loader.load_code_files([directory], ["*.java", "pom.xml"])

    generator = CodeImageGenerator(400, 300, 3, 5)

    composer = HtmlImageComposer(
        output_directory="../output/html_output",
        columns=20,
        thumbnail_size=(500, 1000)
    )

    for file in found_files:
        image = generator.generate_image(file)
        composer.add_image(image, file)

    composer.generate_html()
