from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class Withdrawal:
    amount: float
    transaction_id: str
    withdraw_id: Optional[str] = None
    user_id: Optional[int] = None
    receive: Optional[float] = None
    receive_amount: Optional[float] = None
    receive_amount_coin: Optional[float] = None
    fee_to_apply: Optional[float] = None
    payment_method: Optional[str] = None
    coin: Optional[str] = None
    details: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    id: Optional[int] = None

    def __post_init__(self):
        self.amount = float(str(self.amount))
        self.transaction_id = str(self.transaction_id)

    @classmethod
    def from_json(cls, json: Any) -> "Withdrawal":
        data = json
        if "data" in json and isinstance(json["data"], dict):
            data = json["data"]
        return parse_json(cls, **data)
