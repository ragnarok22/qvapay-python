from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from dateutil.parser import parse

from ..utils import parse_json


@dataclass
class Transaction:
    """
    QvaPay transaction
    """

    id: UUID  # alias: uuid
    app_id: int
    amount: float
    description: str
    remote_id: str
    status: str
    created_at: datetime
    updated_at: datetime
    signed: Optional[int]

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.app_id = int(str(self.app_id))
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.remote_id = str(self.remote_id)
        self.status = str(self.status)
        self.created_at = parse(str(self.created_at))
        self.updated_at = parse(str(self.updated_at))
        self.signed = int(str(self.signed)) if self.signed is not None else None

    @classmethod
    def from_json(cls, json: Any) -> "Transaction":
        json["id"] = json["uuid"]
        del json["uuid"]
        signed = json["signed"] if "signed" in json else None
        return parse_json(cls, **json, signed=signed)
