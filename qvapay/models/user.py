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
    address: Optional[str] = None
    image: Optional[str] = None
    cover: Optional[str] = None
    balance: Optional[str] = None
    pending_balance: Optional[str] = None
    satoshis: Optional[int] = None
    phone: Optional[str] = None
    phone_verified: Optional[bool] = None
    telegram: Optional[str] = None
    twitter: Optional[str] = None
    kyc: Optional[bool] = None
    vip: Optional[bool] = None
    golden_check: Optional[bool] = None
    pin: Optional[int] = None
    last_seen: Optional[str] = None
    telegram_id: Optional[str] = None
    role: Optional[str] = None
    p2p_enabled: Optional[bool] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.username = str(self.username)
        self.name = str(self.name)
        self.email = str(self.email)

    @classmethod
    def from_json(cls, json: Any) -> "User":
        aliases = {"createdAt": "created_at", "updatedAt": "updated_at"}
        mapped = {aliases.get(k, k): v for k, v in json.items()}
        return parse_json(cls, **mapped)
