from dataclasses import dataclass
from typing import Any
from uuid import UUID


@dataclass
class Invoice:
    """
    QvaPay invoice
    """

    app_id: UUID
    transation_id: UUID  # alias: transation_uuid
    amount: float
    description: str
    remote_id: str
    signed: int
    url: str  # AnyUrl
    signed_url: str  # AnyUrl alias: signedUrl

    def __post_init__(self):
        self.app_id = UUID(str(self.app_id))
        self.transation_id = UUID(str(self.transation_id))
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.remote_id = str(self.remote_id)
        self.signed = int(str(self.signed))
        self.url = str(self.url)
        self.signed_url = str(self.signed_url)

    @staticmethod
    def from_json(json: Any) -> "Invoice":
        json["transation_id"] = json["transation_uuid"]
        json["signed_url"] = json["signedUrl"]
        del json["transation_uuid"]
        del json["signedUrl"]
        return Invoice(**json)
