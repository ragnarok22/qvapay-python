from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class PaymentLink:
    name: str
    product_id: str
    amount: str
    payment_link_url: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.name = str(self.name)
        self.product_id = str(self.product_id)

    @classmethod
    def from_json(cls, json: Any) -> "PaymentLink":
        return parse_json(cls, **json)
