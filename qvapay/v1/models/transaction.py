from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from dateutil.parser import parse


@dataclass
class Transaction:
    """
    QvaPay transaction
    """

    id: UUID  # alias: uuid
    user_id: int
    app_id: int
    amount: float
    description: str
    remote_id: str
    status: str
    paid_by_user_id: int
    created_at: datetime
    updated_at: datetime
    signed: Optional[int]

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.user_id = int(str(self.user_id))
        self.app_id = int(str(self.app_id))
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.remote_id = str(self.remote_id)
        self.status = str(self.status)
        self.paid_by_user_id = int(str(self.paid_by_user_id))
        self.created_at = parse(str(self.created_at))
        self.updated_at = parse(str(self.updated_at))
        self.signed = int(str(self.signed)) if self.signed is not None else None

    @staticmethod
    def from_json(json: Any) -> "Transaction":
        json["id"] = json["uuid"]
        del json["uuid"]
        return Transaction(**json, signed=json["signed"] if "signed" in json else None)
