from dataclasses import dataclass
from typing import Any
from uuid import UUID

from ..utils import parse_json


@dataclass
class Service:
    id: UUID  # alias: uuid
    name: str
    description: str
    logo: str

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.name = str(self.name)
        self.description = str(self.description)
        self.logo = str(self.logo)

    @classmethod
    def from_json(cls, json: Any) -> "Service":
        json["id"] = json["uuid"]
        del json["uuid"]
        return parse_json(cls, **json)
