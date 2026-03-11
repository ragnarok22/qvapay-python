from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class Withdrawal:
    uuid: str
    amount: float
    status: str
    pay_method: str
    details: str
    created_at: str
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.amount = float(str(self.amount))
        self.status = str(self.status)

    @classmethod
    def from_json(cls, json: Any) -> "Withdrawal":
        return parse_json(cls, **json)
