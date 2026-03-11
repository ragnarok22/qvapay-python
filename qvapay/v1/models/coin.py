from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Coin:
    name: str
    code: str
    logo: str

    def __post_init__(self):
        self.name = str(self.name)
        self.code = str(self.code)
        self.logo = str(self.logo)

    @classmethod
    def from_json(cls, json: Any) -> "Coin":
        return parse_json(cls, **json)
