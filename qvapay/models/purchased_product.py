from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class PurchasedProduct:
    amount: float
    status: str
    id: Optional[int] = None
    service_id: Optional[int] = None
    service_data: Optional[str] = None
    notes: Optional[str] = None
    transaction_id: Optional[int] = None
    notified: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.amount = float(str(self.amount))
        if self.id is not None:
            self.id = int(self.id)
        if self.service_id is not None:
            self.service_id = int(self.service_id)
        if self.transaction_id is not None:
            self.transaction_id = int(self.transaction_id)

    @classmethod
    def from_json(cls, json: Any) -> "PurchasedProduct":
        return parse_json(cls, **json)
