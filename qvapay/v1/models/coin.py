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
    trade: bool
    stable: bool
    decimals: int
    fee_in: str
    fee_out: str
    min_in: str
    min_out: str
    max_in: float
    max_out: float
    description: Optional[str]

    def __post_init__(self):
        self.id = str(self.id)
        self.name = str(self.name)
        self.logo = str(self.logo)
        self.tick = str(self.tick)
        self.price = str(self.price)
        self.enabled_in = bool(self.enabled_in)
        self.enabled_out = bool(self.enabled_out)
        self.enabled_p2p = bool(self.enabled_p2p)
        self.trade = bool(self.trade)
        self.stable = bool(self.stable)
        self.decimals = int(str(self.decimals))
        self.fee_in = str(self.fee_in)
        self.fee_out = str(self.fee_out)
        self.min_in = str(self.min_in)
        self.min_out = str(self.min_out)
        self.max_in = float(str(self.max_in))
        self.max_out = float(str(self.max_out))

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
        for coin in self.coins:
            coin.__post_init__()

    @classmethod
    def from_json(cls, json: Any) -> "CoinCategory":
        data = {**json}
        coins = [Coin.from_json(c) for c in data.pop("Coins", [])]
        return parse_json(cls, **data, coins=coins)
