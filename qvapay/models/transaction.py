from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from typing import List

from dataclasses_json import config, dataclass_json

from .info import Info
from .owner import Owner
from .paid import PaidBy


@dataclass
@dataclass_json
class Transaction:
    """
    QvaPay transaction
    """

    id: UUID = field(metadata=config(field_name="uuid"))
    user_id: int
    app_id: int
    amount: float
    description: str
    remote_id: str
    status: str
    paid_by_user_id: int
    signed: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if self.signed == 1:
            self.signed = True
        else:
            self.signed = False


@dataclass
@dataclass_json
class TransactionDetal(Transaction):
    """
    QvaPay transaction
    """

    paid_by: PaidBy
    app: Info
    owner: Owner


@dataclass
@dataclass_json
class PaginatedTransactions:
    current_page: int
    data: List[Transaction]
    first_page_url: str
    from_index: int = field(metadata=config(field_name="from"))
    last_page: int
    last_page_url: str
    next_page_url: str
    path: str
    per_page: int
    prev_page_url: int
    to_index: int = field(metadata=config(field_name="to"))
    total: int
