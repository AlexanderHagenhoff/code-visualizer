
from file_finder.file_finder import FileFinder
from image_generation.code_image_generator import CodeImageGenerator

if __name__ == "__main__":
    directory = r'D:\dev\spring-boot\spring-boot-project\spring-boot-actuator'

    file_finder = FileFinder(directory)
    found_files = file_finder.find_files(["*.java"])

    for found_file in found_files:
        print(found_file)

    file_path = found_file
    output_image_path = "output_image.png"

    generator = CodeImageGenerator(file_path, 200, 1000)
    generator.generate_image()
    generator.save_image(output_image_path)


