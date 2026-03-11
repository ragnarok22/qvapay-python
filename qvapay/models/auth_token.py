from dataclasses import dataclass
from typing import Any

from ..utils import parse_json


@dataclass
class AuthToken:
    access_token: str
    token_type: str = "Bearer"

    def __post_init__(self):
        self.access_token = str(self.access_token)
        self.token_type = str(self.token_type)

    @classmethod
    def from_json(cls, json: Any) -> "AuthToken":
        return parse_json(cls, **json)
