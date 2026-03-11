from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from dateutil.parser import parse

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
        self.created_at = parse(str(self.created_at))
        self.updated_at = parse(str(self.updated_at))

    @classmethod
    def from_json(cls, json: Any) -> "Withdrawal":
        json["id"] = json["uuid"]
        del json["uuid"]
        return parse_json(cls, **json)
