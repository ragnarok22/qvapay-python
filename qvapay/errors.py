from dataclasses import dataclass
from typing import Optional


@dataclass
class QvaPayError(Exception):
    status_code: int
    status_message: Optional[str] = None

    def __str__(self) -> str:
        return f"({self.status_code}, {self.status_message})"
