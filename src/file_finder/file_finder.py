from pathlib import Path


class FileFinder:
    DIRECTORY_NOT_FOUND_ERROR = "The directory {directory} does not exist."
    EMPTY_FILE_PATTERN_ERROR = "No file patterns provided. Please provide at least one file pattern."

    def __init__(self, directory):
        self.directory = Path(directory)

    def find_files(self, extensions):
        if not self.directory.exists():
            raise FileNotFoundError(self.DIRECTORY_NOT_FOUND_ERROR.format(directory=self.directory))

        if not extensions:
            raise ValueError(self.EMPTY_FILE_PATTERN_ERROR)

        files = []
        for ext in extensions:
            self.add_file_by_extension(files, ext)

        return files

    def add_file_by_extension(self, files, ext):
        for file in self.directory.rglob(ext):
            files.append(file)
