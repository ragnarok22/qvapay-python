from dataclasses import dataclass
from typing import Any, List, Optional

from ..utils import parse_json


@dataclass
class Transaction:
    uuid: str
    amount: float
    description: str
    remote_id: str
    status: str
    created_at: str
    updated_at: str
    signed: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.status = str(self.status)

    @classmethod
    def from_json(cls, json: Any) -> "Transaction":
        return parse_json(cls, **json)


@dataclass
class PaginatedTransactions:
    current_page: int
    data: List[Transaction]
    total: int

    def __post_init__(self):
        self.current_page = int(str(self.current_page))
        self.total = int(str(self.total))

    @classmethod
    def from_json(cls, json: Any) -> "PaginatedTransactions":
        data = {**json}
        transactions = [
            Transaction.from_json(t) for t in data.pop("data", [])
        ]
        return parse_json(cls, **data, data=transactions)


@dataclass
class TransactionDetail(Transaction):
    app_id: Optional[str] = None
    paid_by_user_id: Optional[str] = None

    @classmethod
    def from_json(cls, json: Any) -> "TransactionDetail":
        return parse_json(cls, **json)
