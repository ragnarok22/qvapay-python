from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QvaPayError(Exception):
    status_code: int
    status_message: Optional[str] = field(default=None)

    def __str__(self) -> str:
        if self.status_message:
            return f"QvaPayError({self.status_code}): {self.status_message}"
        return f"QvaPayError({self.status_code})"
