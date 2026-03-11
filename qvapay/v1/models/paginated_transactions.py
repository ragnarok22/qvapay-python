from dataclasses import dataclass
from typing import Any, List, Optional

from ..utils import parse_json
from .link import Link
from .transaction import Transaction


@dataclass
class PaginatedTransactions:
    current_page: int
    last_page: int
    from_index: int  # alias: from
    to_index: int  # alias: to
    per_page: int
    total: int
    first_page_url: str  # AnyUrl
    last_page_url: str  # AnyUrl
    prev_page_url: Optional[str]  # Optional[AnyUrl]
    next_page_url: Optional[str]  # Optional[AnyUrl]
    path: str
    links: List[Link]
    data: List[Transaction]

    def __post_init__(self):
        self.current_page = int(str(self.current_page))
        self.last_page = int(str(self.last_page))
        self.from_index = int(str(self.from_index))
        self.to_index = int(str(self.to_index))
        self.per_page = int(str(self.per_page))
        self.total = int(str(self.total))
        self.first_page_url = str(self.first_page_url)
        self.last_page_url = str(self.last_page_url)
        self.prev_page_url = (
            str(self.prev_page_url) if self.prev_page_url is not None else None
        )
        self.next_page_url = (
            str(self.next_page_url) if self.next_page_url is not None else None
        )
        self.path = str(self.path)
        for link in self.links:
            link.__post_init__()
        for item in self.data:
            item.__post_init__()

    @classmethod
    def from_json(cls, json: Any) -> "PaginatedTransactions":
        data = {**json}
        data["from_index"] = data.pop("from")
        data["to_index"] = data.pop("to")
        links = [Link.from_json(item) for item in data.pop("links")]
        transactions = [Transaction.from_json(item) for item in data.pop("data")]
        return parse_json(cls, **data, links=links, data=transactions)
