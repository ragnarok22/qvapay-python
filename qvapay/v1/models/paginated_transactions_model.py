from typing import List, Optional

from pydantic import AnyUrl, BaseModel, Field

from .link_model import LinkModel
from .transaction_model import TransactionModel


class PaginatedTransactionsModel(BaseModel):
    current_page: int
    last_page: int
    from_index: int = Field(alias="from")
    to_index: int = Field(alias="to")
    per_page: int
    total: int
    first_page_url: AnyUrl
    last_page_url: AnyUrl
    prev_page_url: Optional[AnyUrl]
    next_page_url: Optional[AnyUrl]
    path: str
    links: List[LinkModel]
    data: List[TransactionModel]
