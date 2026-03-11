from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class Domain:
    domain: str
    available: bool

    def __post_init__(self):
        self.domain = str(self.domain)
        self.available = bool(self.available)

    @classmethod
    def from_json(cls, json: Any) -> "Domain":
        return parse_json(cls, **json)
