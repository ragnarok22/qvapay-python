from importlib.metadata import version

from ._async import auth, coins, stocks
from ._async.client import AsyncQvaPayClient
from ._async.merchant import AsyncQvaPayMerchant
from ._sync.client import SyncQvaPayClient
from ._sync.merchant import SyncQvaPayMerchant
from .errors import QvaPayError
from .models.app import App
from .models.auth_token import AuthToken
from .models.coin import Coin, CoinCategory
from .models.contact import Contact
from .models.domain import Domain
from .models.invoice import Invoice
from .models.p2p import P2PMessage, P2POffer
from .models.payment_link import PaymentLink
from .models.payment_method import PaymentMethod
from .models.product import Product
from .models.transaction import (
    PaginatedTransactions,
    Transaction,
    TransactionDetail,
)
from .models.user import User
from .models.withdrawal import Withdrawal

__version__ = version("qvapay")
__author__ = "Reinier Hernández <me@reinierhernandez.com>"
__all__ = [
    "AsyncQvaPayClient",
    "AsyncQvaPayMerchant",
    "SyncQvaPayClient",
    "SyncQvaPayMerchant",
    "QvaPayError",
    "auth",
    "coins",
    "stocks",
    "App",
    "AuthToken",
    "Coin",
    "CoinCategory",
    "Contact",
    "Domain",
    "Invoice",
    "P2PMessage",
    "P2POffer",
    "PaginatedTransactions",
    "PaymentLink",
    "PaymentMethod",
    "Product",
    "Transaction",
    "TransactionDetail",
    "User",
    "Withdrawal",
]
