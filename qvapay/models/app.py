from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class App:
    uuid: str
    name: str
    logo: str
    url: str
    desc: str
    callback: str
    success_url: str
    cancel_url: str
    enabled: bool
    active: bool
    secret: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.name = str(self.name)
        self.enabled = bool(self.enabled)
        self.active = bool(self.active)

    @classmethod
    def from_json(cls, json: Any) -> "App":
        return parse_json(cls, **json)
