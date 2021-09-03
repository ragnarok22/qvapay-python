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

    @staticmethod
    def from_json(json: Any) -> "TransactionDetail":
        paid_by = PaidBy.from_json(json["paid_by"])
        app = Info.from_json(json["app"])
        owner = Owner.from_json(json["owner"])
        del json["paid_by"]
        del json["app"]
        del json["owner"]
        base = Transaction.from_json(json)
        return TransactionDetail(
            id=base.id,
            user_id=base.user_id,
            app_id=base.app_id,
            amount=base.amount,
            description=base.description,
            remote_id=base.remote_id,
            status=base.status,
            paid_by_user_id=base.paid_by_user_id,
            created_at=base.created_at,
            updated_at=base.updated_at,
            signed=base.signed,
            paid_by=paid_by,
            app=app,
            owner=owner,
        )
