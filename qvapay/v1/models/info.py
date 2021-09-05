from dataclasses import dataclass
from datetime import datetime
from typing import Any
from uuid import UUID

from dateutil.parser import parse


@dataclass
class Info:
    """
    QvaPay app info
    """

    id: UUID  # alias: uuid
    user_id: int
    name: str
    url: str  # AnyUrl
    description: str  # alias: desc
    callback: str
    success_url: str  # AnyUrl
    cancel_url: str  # AnyUrl
    logo: str
    active: bool
    enabled: bool
    card: int
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.user_id = int(str(self.user_id))
        self.name = str(self.name)
        self.url = str(self.url)
        self.description = str(self.description)
        self.callback = str(self.callback)
        self.success_url = str(self.success_url)
        self.cancel_url = str(self.cancel_url)
        self.logo = str(self.logo)
        self.active = bool(str(self.active))
        self.enabled = bool(str(self.enabled))
        self.card = int(str(self.card))
        self.created_at = parse(str(self.created_at))
        self.updated_at = parse(str(self.updated_at))

    @staticmethod
    def from_json(json: Any) -> "Info":
        json["id"] = json["uuid"]
        json["description"] = json["desc"]
        del json["uuid"]
        del json["desc"]
        return Info(**json)
