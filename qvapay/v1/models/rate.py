from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Rate:
    name: str
    code: str
    buy: float
    sell: float
    logo: str

    def __post_init__(self):
        self.name = str(self.name)
        self.code = str(self.code)
        self.buy = float(str(self.buy))
        self.sell = float(str(self.sell))
        self.logo = str(self.logo)

    @classmethod
    def from_json(cls, json: Any) -> "Rate":
        return parse_json(cls, **json)
