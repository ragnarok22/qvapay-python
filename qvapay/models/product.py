from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class Product:
    uuid: str
    name: str
    description: str
    price: float
    logo: Optional[str] = None
    category: Optional[str] = None
    created_at: Optional[str] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.name = str(self.name)
        self.price = float(str(self.price))

    @classmethod
    def from_json(cls, json: Any) -> "Product":
        return parse_json(cls, **json)
