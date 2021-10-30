from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class PaidBy:
    username: str
    name: str
    logo: str

    def __post_init__(self):
        self.username = str(self.username)
        self.name = str(self.name)
        self.logo = str(self.logo)

    @classmethod
    def from_json(cls, json: Any) -> "PaidBy":
        return parse_json(cls, **json)
