from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from dateutil.parser import parse

from ..utils import parse_json


@dataclass
class User:
    id: UUID  # alias: uuid
    username: str
    name: str
    lastname: str
    email: str
    bio: Optional[str]
    logo: str
    kyc: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.username = str(self.username)
        self.name = str(self.name)
        self.lastname = str(self.lastname)
        self.email = str(self.email)
        self.bio = str(self.bio) if self.bio is not None else None
        self.logo = str(self.logo)
        self.kyc = bool(self.kyc)
        self.created_at = parse(str(self.created_at))
        self.updated_at = parse(str(self.updated_at))

    @classmethod
    def from_json(cls, json: Any) -> "User":
        json["id"] = json["uuid"]
        del json["uuid"]
        return parse_json(cls, **json)
