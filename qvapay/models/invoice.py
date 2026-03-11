from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class Invoice:
    app_id: str
    amount: str
    description: str
    remote_id: str
    signed: str
    transation_uuid: str
    url: str
    signedUrl: Optional[str] = None

    def __post_init__(self):
        self.app_id = str(self.app_id)
        self.amount = str(self.amount)
        self.description = str(self.description)

    @classmethod
    def from_json(cls, json: Any) -> "Invoice":
        return parse_json(cls, **json)
