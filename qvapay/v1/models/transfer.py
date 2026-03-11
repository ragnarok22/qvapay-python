from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from ..utils import parse_json


@dataclass
class Transfer:
    id: UUID  # alias: uuid
    amount: float
    description: str
    status: str
    created_at: datetime

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.status = str(self.status)
        self.created_at = datetime.fromisoformat(str(self.created_at))

    @classmethod
    def from_json(cls, json: Any) -> "Transfer":
        json["id"] = json["uuid"]
        del json["uuid"]
        return parse_json(cls, **json)
