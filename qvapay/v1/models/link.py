from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class Link:
    url: Optional[str]  # Optional[AnyUrl]
    label: str
    active: bool

    def __post_init__(self):
        self.url = str(self.url) if self.url is not None else None
        self.label = str(self.label)
        self.active = bool(str(self.active))

    @classmethod
    def from_json(cls, json: Any) -> "Link":
        return parse_json(cls, **json)
