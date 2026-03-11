from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from dateutil.parser import parse

from ..utils import parse_json


@dataclass
class PaymentLink:
    id: UUID  # alias: uuid
    amount: float
    description: str
    url: str
    created_at: datetime

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.url = str(self.url)
        self.created_at = parse(str(self.created_at))

    @classmethod
    def from_json(cls, json: Any) -> "PaymentLink":
        json["id"] = json["uuid"]
        del json["uuid"]
        return parse_json(cls, **json)
