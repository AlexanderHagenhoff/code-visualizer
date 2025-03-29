from image_generation.code_image_generator import CodeImageGenerator
from src.code_handling.file_system_loader import FileSystemLoader
from src.image_composition.image_concatenator import ImageConcatenator

if __name__ == "__main__":
    directory = r'D:\dev\spring-boot\spring-boot-project\spring-boot-actuator'

    urls = [
        "https://github.com/AlexanderHagenhoff/spring-boot-postgres-archetype"
    ]

    output_image_path = "output_image.png"

    loader = FileSystemLoader()
    found_files = loader.load_code_files([directory], ["*.java", "pom.xml"])

    generator = CodeImageGenerator(500, 1000, 3, 5)

    concatenator = ImageConcatenator(
        columns=20,
        max_thumbnail_size=(150, 150)
    )

    for file in found_files:
        image = generator.generate_image(file)
        concatenator.add_image(image)

    result_image = concatenator.concatenate()
    result_image.save("combined_result.png")
