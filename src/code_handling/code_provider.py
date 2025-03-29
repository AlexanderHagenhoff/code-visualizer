from abc import abstractmethod
from typing import List

from src.code_handling.code_file import CodeFile


class CodeProvider:

    @abstractmethod
    def load_code_files(self, file_source: List[str], file_pattern: List[str]) -> List[CodeFile]:
        pass
