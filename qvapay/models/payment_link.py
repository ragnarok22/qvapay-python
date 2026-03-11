from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class PaymentLink:
    uuid: str
    amount: float
    description: str
    url: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.amount = float(str(self.amount))
        self.description = str(self.description)

    @classmethod
    def from_json(cls, json: Any) -> "PaymentLink":
        return parse_json(cls, **json)
