from dataclasses import dataclass
from typing import Any, Optional

from ..utils import parse_json


@dataclass
class WithdrawTransaction:
    uuid: str
    app_id: int
    amount: str
    description: str
    remote_id: str
    status: str
    created_at: str
    updated_at: str

    @classmethod
    def from_json(cls, json: Any) -> "WithdrawTransaction":
        return parse_json(cls, **json)


@dataclass
class WithdrawCoin:
    id: int
    name: str
    logo: str
    tick: str
    fee_in: str
    fee_out: str
    min_in: str
    min_out: str
    price: str
    coins_categories_id: Optional[int] = None

    @classmethod
    def from_json(cls, json: Any) -> "WithdrawCoin":
        return parse_json(cls, **json)


@dataclass
class Withdrawal:
    amount: float
    transaction_id: str
    id: Optional[int] = None
    withdraw_id: Optional[str] = None
    user_id: Optional[int] = None
    receive: Optional[float] = None
    receive_amount: Optional[float] = None
    receive_amount_coin: Optional[float] = None
    fee_to_apply: Optional[float] = None
    payment_method: Optional[str] = None
    coin: Optional[str] = None
    details: Optional[str] = None
    status: Optional[str] = None
    tx_id: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    transaction: Optional[WithdrawTransaction] = None
    coin_detail: Optional[WithdrawCoin] = None

    def __post_init__(self):
        self.amount = float(str(self.amount))
        self.transaction_id = str(self.transaction_id)

    @classmethod
    def from_json(cls, json: Any) -> "Withdrawal":
        data = json
        if "data" in json and isinstance(json["data"], dict):
            data = json["data"]
        data = {**data}

        transaction = data.pop("transaction", None)
        if transaction and isinstance(transaction, dict):
            transaction = WithdrawTransaction.from_json(transaction)

        coin_raw = data.pop("coin", None)
        coin_detail = None
        coin_str = None
        if isinstance(coin_raw, dict):
            coin_detail = WithdrawCoin.from_json(coin_raw)
        elif coin_raw is not None:
            coin_str = str(coin_raw)

        return parse_json(
            cls,
            **data,
            transaction=transaction,
            coin_detail=coin_detail,
            coin=coin_str,
        )
