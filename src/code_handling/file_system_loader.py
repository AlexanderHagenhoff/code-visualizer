from src.code_handling.code_file import CodeFile

class FileSystemLoader:

    def load_code_files(self, file_paths: list[str]) -> list[CodeFile]:
        return [self.load_code_file(path) for path in file_paths]

    def load_code_file(self, file_path: str) -> CodeFile:
        with open(file_path, 'r') as f:
            return CodeFile(content=f.read(), filename=file_path)
