from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils import parse_json


@dataclass
class P2POffer:
    id: UUID  # alias: uuid
    coin: str
    amount: float
    price: float
    type: str
    owner: str

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.coin = str(self.coin)
        self.amount = float(str(self.amount))
        self.price = float(str(self.price))
        self.type = str(self.type)
        self.owner = str(self.owner)

    @classmethod
    def from_json(cls, json: Any) -> "P2POffer":
        json["id"] = json["uuid"]
        del json["uuid"]
        return parse_json(cls, **json)
