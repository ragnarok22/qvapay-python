from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class P2POffer:
    uuid: str
    coin: str
    amount: float
    price: float
    type: str
    status: str
    owner: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.amount = float(str(self.amount))
        self.price = float(str(self.price))

    @classmethod
    def from_json(cls, json: Any) -> "P2POffer":
        return parse_json(cls, **json)


@dataclass
class P2PMessage:
    uuid: str
    message: str
    sender: str
    created_at: str

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.message = str(self.message)

    @classmethod
    def from_json(cls, json: Any) -> "P2PMessage":
        return parse_json(cls, **json)
