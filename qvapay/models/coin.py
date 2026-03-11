from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, List, Optional

from ..utils import parse_json


@dataclass
class CoinCategory:
    id: int
    name: str
    logo: str
    coins: List[Coin] = field(default_factory=list)

    def __post_init__(self):
        self.id = int(str(self.id))
        self.name = str(self.name)
        self.logo = str(self.logo)

    @classmethod
    def from_json(cls, json: Any) -> CoinCategory:
        data = {**json}
        raw_coins = data.pop("coins", data.pop("Coins", []))
        coins = [Coin.from_json(c) for c in raw_coins]
        return parse_json(cls, **data, coins=coins)


@dataclass
class Coin:
    id: str
    name: str
    logo: str
    tick: str
    price: str
    enabled_in: bool
    enabled_out: bool
    enabled_p2p: bool
    fee_in: str
    fee_out: str
    min_in: str
    min_out: str
    coins_categories_id: Optional[int] = None
    max_in: Optional[float] = None
    max_out: Optional[float] = None
    network: Optional[str] = None
    working_data: Optional[str] = None
    coin_category: Optional[CoinCategory] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.id = str(self.id)
        self.name = str(self.name)
        self.enabled_in = bool(self.enabled_in)
        self.enabled_out = bool(self.enabled_out)
        self.enabled_p2p = bool(self.enabled_p2p)
        if self.max_in is not None:
            self.max_in = float(str(self.max_in))
        if self.max_out is not None:
            self.max_out = float(str(self.max_out))

    @classmethod
    def from_json(cls, json: Any) -> Coin:
        data = {**json}
        raw_category = data.pop("coin_category", None)
        category = CoinCategory.from_json(raw_category) if raw_category else None
        return parse_json(cls, **data, coin_category=category)
