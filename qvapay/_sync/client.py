from dataclasses import dataclass, field

from ..http import BASE_URL, DEFAULT_TIMEOUT, SyncClient, TimeoutTypes
from .modules.app import AppModule
from .modules.p2p import P2PModule
from .modules.payment_links import PaymentLinksModule
from .modules.store import StoreModule
from .modules.transactions import TransactionsModule
from .modules.user import UserModule
from .modules.withdraw import WithdrawModule


@dataclass
class SyncQvaPayClient:
    """
    QvaPay user client authenticated with a Bearer token.
    * access_token: Bearer token obtained from login.
    """

    access_token: str
    timeout: TimeoutTypes = field(default_factory=lambda: DEFAULT_TIMEOUT)

    def __post_init__(self):
        self._http = SyncClient(
            base_url=BASE_URL,
            headers={"Authorization": f"Bearer {self.access_token}"},
            timeout=self.timeout,
            follow_redirects=True,
        )
        self.app = AppModule(self._http)
        self.transactions = TransactionsModule(self._http)
        self.withdraw = WithdrawModule(self._http)
        self.user = UserModule(self._http)
        self.p2p = P2PModule(self._http)
        self.payment_links = PaymentLinksModule(self._http)
        self.store = StoreModule(self._http)

    def __enter__(self) -> "SyncQvaPayClient":
        return self

    def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self._http.aclose()
