from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Stock:
    key: str
    buy: float
    sell: float

    def __post_init__(self):
        self.key = str(self.key)
        self.buy = float(str(self.buy))
        self.sell = float(str(self.sell))

    @classmethod
    def from_json(cls, json: Any) -> "Stock":
        return parse_json(cls, **json)
