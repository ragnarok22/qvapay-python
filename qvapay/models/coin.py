from dataclasses import dataclass
from typing import Any, List, Optional

from ..utils import parse_json


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
    network: Optional[str] = None
    working_data: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.id = str(self.id)
        self.name = str(self.name)
        self.enabled_in = bool(self.enabled_in)
        self.enabled_out = bool(self.enabled_out)
        self.enabled_p2p = bool(self.enabled_p2p)

    @classmethod
    def from_json(cls, json: Any) -> "Coin":
        return parse_json(cls, **json)


@dataclass
class CoinCategory:
    id: int
    name: str
    logo: str
    coins: List[Coin]

    def __post_init__(self):
        self.id = int(str(self.id))
        self.name = str(self.name)
        self.logo = str(self.logo)

    @classmethod
    def from_json(cls, json: Any) -> "CoinCategory":
        data = {**json}
        raw_coins = data.pop("coins", data.pop("Coins", []))
        coins = [Coin.from_json(c) for c in raw_coins]
        return parse_json(cls, **data, coins=coins)
