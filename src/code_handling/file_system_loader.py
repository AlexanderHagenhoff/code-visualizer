import os
import fnmatch
from typing import List, Iterable
from pathlib import Path

from src.code_handling.CodeProvider import CodeProvider
from src.code_handling.code_file import CodeFile


class FileSystemLoader(CodeProvider):

    def load_code_files(self, source_paths: List[str], file_patterns: List[str]) -> List[CodeFile]:
        code_files = []
        for path in source_paths:
            code_files.extend(self._process_path(path, file_patterns))
        return code_files

    def _process_path(self, path: str, file_patterns: List[str]) -> List[CodeFile]:
        resolved_path = Path(path).resolve()

        if not resolved_path.exists():
            return []

        if resolved_path.is_file():
            return self._process_single_file(resolved_path, file_patterns)

        if resolved_path.is_dir():
            return self._process_directory(resolved_path, file_patterns)

        return []

    def _process_single_file(self, file_path: Path, file_patterns: List[str]) -> List[CodeFile]:
        if self._filename_matches_patterns(file_path.name, file_patterns):
            return [self._load_file_content(file_path)]
        return []

    def _process_directory(self, directory: Path, file_patterns: List[str]) -> List[CodeFile]:
        matched_files = []
        for root, _, filenames in os.walk(directory):
            matched_files.extend(
                self._find_matching_files(Path(root), filenames, file_patterns)
            )
        return matched_files

    def _find_matching_files(self, directory: Path, filenames: Iterable[str], file_patterns: List[str]) -> List[CodeFile]:
        return [
            self._load_file_content(directory / filename)
            for filename in filenames
            if self._filename_matches_patterns(filename, file_patterns)
        ]

    def _load_file_content(self, file_path: Path) -> CodeFile:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return CodeFile(content=file.read(), filename=str(file_path))
        except UnicodeDecodeError:
            return CodeFile(content="", filename=str(file_path))

    def _filename_matches_patterns(self, filename: str, patterns: List[str]) -> bool:
        return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)