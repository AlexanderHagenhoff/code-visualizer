from abc import abstractmethod
from typing import List

from src.main.python.code_loading.code_file import CodeFile


class CodeLoader:
    @abstractmethod
    def load_code_files(
        self,
        file_source: List[str],
        file_pattern: List[str],
        ignore_patterns: List[str] = None
    ) -> List[CodeFile]:
        pass
