from code_handling.file_system_file_finder import FileSystemFileFinder
from image_generation.code_image_generator import CodeImageGenerator
from src.code_handling.file_system_loader import FileSystemLoader

if __name__ == "__main__":
    directory = r'D:\dev\spring-boot\spring-boot-project\spring-boot-actuator'

    file_finder = FileSystemFileFinder(directory)
    found_files = file_finder.find_files(["*.java"])

    for found_file in found_files:
        print(found_file)

    output_image_path = "output_image.png"

    loader = FileSystemLoader()
    code_files = loader.load_code_files(found_files)

    generator = CodeImageGenerator(500, 1000, 10)
    image = generator.generate_image(code_files[0])
    image.save("expected_simple_file_result.png")
