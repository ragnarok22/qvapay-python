from dataclasses import dataclass
from typing import Any, List, Optional

from ..utils import parse_json


@dataclass
class TransactionApp:
    name: str
    logo: str = ""
    url: str = ""

    @classmethod
    def from_json(cls, json: Any) -> "TransactionApp":
        return parse_json(cls, **json)


@dataclass
class TransactionUser:
    name: str
    username: str = ""
    uuid: Optional[str] = None
    lastname: Optional[str] = None
    bio: Optional[str] = None
    logo: Optional[str] = None
    kyc: Optional[int] = None

    @classmethod
    def from_json(cls, json: Any) -> "TransactionUser":
        return parse_json(cls, **json)


@dataclass
class Wallet:
    transaction_id: int
    wallet_type: str
    wallet: str
    value: str
    received: str
    status: str
    created_at: str
    invoice_id: Optional[str] = None
    txid: Optional[str] = None
    updated_at: Optional[str] = None

    def __post_init__(self):
        self.transaction_id = int(self.transaction_id)

    @classmethod
    def from_json(cls, json: Any) -> "Wallet":
        return parse_json(cls, **json)


@dataclass
class Service:
    uuid: str
    name: str
    lead: str
    price: str
    logo: str
    sublogo: str = ""
    desc: str = ""

    @classmethod
    def from_json(cls, json: Any) -> "Service":
        return parse_json(cls, **json)


@dataclass
class ServiceBuy:
    service_id: int
    service_data: str
    status: str
    amount: str
    transaction_id: int
    created_at: str
    updated_at: Optional[str] = None
    service: Optional[Service] = None

    def __post_init__(self):
        self.service_id = int(self.service_id)
        self.transaction_id = int(self.transaction_id)

    @classmethod
    def from_json(cls, json: Any) -> "ServiceBuy":
        data = {**json}
        service = data.pop("service", None)
        if service and isinstance(service, dict):
            service = Service.from_json(service)
        return parse_json(cls, **data, service=service)


@dataclass
class Transaction:
    uuid: str
    amount: float
    description: str
    remote_id: str
    status: str
    created_at: str
    updated_at: str
    app_id: Optional[int] = None
    logo: Optional[str] = None
    signed: Optional[str] = None
    app: Optional[TransactionApp] = None
    paid_by: Optional[TransactionUser] = None
    app_owner: Optional[TransactionApp] = None
    owner: Optional[TransactionUser] = None
    wallet: Optional[Wallet] = None
    servicebuy: Optional[ServiceBuy] = None

    def __post_init__(self):
        self.uuid = str(self.uuid)
        self.amount = float(str(self.amount))
        self.description = str(self.description)
        self.status = str(self.status)

    @classmethod
    def from_json(cls, json: Any) -> "Transaction":
        data = {**json}

        app = data.pop("app", None)
        if app and isinstance(app, dict):
            app = TransactionApp.from_json(app)

        paid_by = data.pop("paid_by", None)
        if paid_by and isinstance(paid_by, dict):
            paid_by = TransactionUser.from_json(paid_by)

        app_owner = data.pop("app_owner", None)
        if app_owner and isinstance(app_owner, dict):
            app_owner = TransactionApp.from_json(app_owner)

        owner = data.pop("owner", None)
        if owner and isinstance(owner, dict):
            owner = TransactionUser.from_json(owner)

        wallet = data.pop("wallet", None)
        if wallet and isinstance(wallet, dict):
            wallet = Wallet.from_json(wallet)

        servicebuy = data.pop("servicebuy", None)
        if servicebuy and isinstance(servicebuy, dict):
            servicebuy = ServiceBuy.from_json(servicebuy)

        return parse_json(
            cls,
            **data,
            app=app,
            paid_by=paid_by,
            app_owner=app_owner,
            owner=owner,
            wallet=wallet,
            servicebuy=servicebuy,
        )


@dataclass
class PaginatedTransactions:
    current_page: int
    data: List[Transaction]
    total: int

    def __post_init__(self):
        self.current_page = int(str(self.current_page))
        self.total = int(str(self.total))

    @classmethod
    def from_json(cls, json: Any) -> "PaginatedTransactions":
        data = {**json}
        transactions = [Transaction.from_json(t) for t in data.pop("data", [])]
        return parse_json(cls, **data, data=transactions)


@dataclass
class TransactionDetail(Transaction):
    paid_by_user_id: Optional[str] = None

    @classmethod
    def from_json(cls, json: Any) -> "TransactionDetail":
        data = {**json}

        app = data.pop("app", None)
        if app and isinstance(app, dict):
            app = TransactionApp.from_json(app)

        paid_by = data.pop("paid_by", None)
        if paid_by and isinstance(paid_by, dict):
            paid_by = TransactionUser.from_json(paid_by)

        app_owner = data.pop("app_owner", None)
        if app_owner and isinstance(app_owner, dict):
            app_owner = TransactionApp.from_json(app_owner)

        owner = data.pop("owner", None)
        if owner and isinstance(owner, dict):
            owner = TransactionUser.from_json(owner)

        wallet = data.pop("wallet", None)
        if wallet and isinstance(wallet, dict):
            wallet = Wallet.from_json(wallet)

        servicebuy = data.pop("servicebuy", None)
        if servicebuy and isinstance(servicebuy, dict):
            servicebuy = ServiceBuy.from_json(servicebuy)

        return parse_json(
            cls,
            **data,
            app=app,
            paid_by=paid_by,
            app_owner=app_owner,
            owner=owner,
            wallet=wallet,
            servicebuy=servicebuy,
        )
