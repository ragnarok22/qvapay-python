from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class Link:
    url: Optional[str]  # Optional[AnyUrl]
    label: str
    active: bool

    def __post_init__(self):
        self.url = str(self.url) if self.url is not None else None
        self.label = str(self.label)
        self.active = bool(str(self.active))

    @staticmethod
    def from_json(json: Any) -> "Link":
        return Link(**json)
