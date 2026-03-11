from dataclasses import dataclass
from typing import Any

from .info import Info
from .owner import Owner
from .paid_by import PaidBy
from .transaction import Transaction


@dataclass
class TransactionDetail(Transaction):
    """
    QvaPay transaction
    """

    paid_by: PaidBy
    app: Info
    owner: Owner

    def __post_init__(self):
        self.paid_by.__post_init__()
        self.app.__post_init__()
        self.owner.__post_init__()
        return super().__post_init__()

    @classmethod
    def from_json(cls, json: Any) -> "TransactionDetail":
        data = {**json}
        paid_by = PaidBy.from_json(data.pop("paid_by"))
        app = Info.from_json(data.pop("app"))
        owner = Owner.from_json(data.pop("owner"))
        base = Transaction.from_json(data)
        return TransactionDetail(
            id=base.id,
            app_id=base.app_id,
            amount=base.amount,
            description=base.description,
            remote_id=base.remote_id,
            status=base.status,
            created_at=base.created_at,
            updated_at=base.updated_at,
            signed=base.signed,
            paid_by=paid_by,
            app=app,
            owner=owner,
        )
