from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from ..utils import parse_json


@dataclass
class Withdrawal:
    id: UUID  # alias: uuid
    amount: float
    status: str
    pay_method: str
    details: str
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.amount = float(str(self.amount))
        self.status = str(self.status)
        self.pay_method = str(self.pay_method)
        self.details = str(self.details)
        self.created_at = datetime.fromisoformat(str(self.created_at))
        self.updated_at = datetime.fromisoformat(str(self.updated_at))

    @classmethod
    def from_json(cls, json: Any) -> "Withdrawal":
        data = {**json}
        data["id"] = data.pop("uuid")
        return parse_json(cls, **data)
