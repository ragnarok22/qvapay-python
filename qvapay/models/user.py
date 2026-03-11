from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class User:
    uuid: str
    username: str
    name: str
    lastname: str
    email: str
    bio: Optional[str] = None
    logo: Optional[str] = None
    kyc: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.username = str(self.username)
        self.name = str(self.name)
        self.email = str(self.email)

    @classmethod
    def from_json(cls, json: Any) -> "User":
        return parse_json(cls, **json)
