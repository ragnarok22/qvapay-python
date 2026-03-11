from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json
from .user import User


@dataclass
class AuthToken:
    access_token: str
    token_type: str = "Bearer"
    me: Optional[User] = None

    def __post_init__(self):
        self.access_token = str(self.access_token)
        self.token_type = str(self.token_type)
        if isinstance(self.me, dict):
            self.me = User.from_json(self.me)

    @classmethod
    def from_json(cls, json: Any) -> "AuthToken":
        aliases = {"accessToken": "access_token"}
        mapped = {aliases.get(k, k): v for k, v in json.items()}
        return parse_json(cls, **mapped)
