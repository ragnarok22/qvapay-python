from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from dataclasses_json import config, dataclass_json

from .info import Info
from .owner import Owner
from .paid import PaidBy
from .link import Link


@dataclass_json
@dataclass
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
    created_at: datetime = field(metadata=config(decoder=str))
    updated_at: datetime = field(metadata=config(decoder=str))


@dataclass_json
@dataclass
class TransactionDetail(Transaction):
    """
    QvaPay transaction
    """

    paid_by: PaidBy
    app: Info
    owner: Owner


@dataclass_json
@dataclass
class PaginatedTransactions:
    current_page: int
    data: List[Transaction]
    first_page_url: str
    from_index: Optional[int] = field(metadata=config(field_name="from"))
    last_page: int
    last_page_url: str
    links: List[Link]
    next_page_url: Optional[str]
    path: str
    per_page: int
    prev_page_url: Optional[str]
    to_index: Optional[int] = field(metadata=config(field_name="to"))
    total: int
