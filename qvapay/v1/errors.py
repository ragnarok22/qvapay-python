from dataclasses import dataclass, field
from typing import Optional


@dataclass
class QvaPayError(Exception):
    status_code: int
    status_message: Optional[str] = field(default=None)
