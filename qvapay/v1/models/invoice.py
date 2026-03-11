from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils import parse_json


@dataclass
class Invoice:
    """
    QvaPay invoice
    """

    app_id: UUID
    transaction_id: UUID  # alias: transation_uuid
    amount: float
    description: str
    remote_id: str
    signed: int
    url: str  # AnyUrl
    signed_url: str  # AnyUrl alias: signedUrl

    def __post_init__(self):
        self.app_id = UUID(str(self.app_id))
        self.transaction_id = UUID(str(self.transaction_id))
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.remote_id = str(self.remote_id)
        self.signed = int(str(self.signed))
        self.url = str(self.url)
        self.signed_url = str(self.signed_url)

    @classmethod
    def from_json(cls, json: Any) -> "Invoice":
        data = {**json}
        data["transaction_id"] = data.pop("transation_uuid")
        data["signed_url"] = data.pop("signedUrl")
        return parse_json(cls, **data)
