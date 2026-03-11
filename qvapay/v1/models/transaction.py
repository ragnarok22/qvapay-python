from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

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
        self.created_at = datetime.fromisoformat(str(self.created_at))
        self.updated_at = datetime.fromisoformat(str(self.updated_at))
        self.signed = int(str(self.signed)) if self.signed is not None else None

    @classmethod
    def from_json(cls, json: Any) -> "Transaction":
        data = {**json}
        data["id"] = data.pop("uuid")
        signed = data.get("signed")
        return parse_json(cls, **data, signed=signed)
