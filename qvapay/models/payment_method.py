from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class PaymentMethod:
    uuid: str
    name: str
    details: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.name = str(self.name)

    @classmethod
    def from_json(cls, json: Any) -> "PaymentMethod":
        return parse_json(cls, **json)
