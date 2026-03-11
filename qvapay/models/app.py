from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class App:
    uuid: str
    name: str
    logo: str
    url: str
    description: str = ""
    callback: str = ""
    success_url: str = ""
    cancel_url: str = ""
    enabled: bool = True
    active: bool = True
    allowed_payment_auth: bool = False
    card: bool = False
    secret: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.name = str(self.name)
        self.enabled = bool(self.enabled)
        self.active = bool(self.active)
        self.card = bool(self.card)

    @classmethod
    def from_json(cls, json: Any) -> "App":
        aliases = {"desc": "description"}
        mapped = {aliases.get(k, k): v for k, v in json.items()}
        return parse_json(cls, **mapped)
