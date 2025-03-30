from dataclasses import dataclass
from typing import Optional


@dataclass
class CodeFile:
    content: str
    filename: Optional[str] = None
