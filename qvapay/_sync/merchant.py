from dataclasses import dataclass, field
from typing import Any

from ..http import BASE_URL, DEFAULT_TIMEOUT, SyncClient, TimeoutTypes
from ..models.app import App
from ..models.invoice import Invoice
from ..models.transaction import PaginatedTransactions
from ..utils import validate_response


@dataclass
class SyncQvaPayMerchant:
    """
    QvaPay merchant client.
    * uuid: QvaPay app UUID.
    * secret_key: QvaPay app secret key.
    Get your credentials at: https://qvapay.com/apps/create
    """

    uuid: str
    secret_key: str
    timeout: TimeoutTypes = field(default_factory=lambda: DEFAULT_TIMEOUT)

    def __post_init__(self):
        self._auth = {
            "app_id": self.uuid,
            "app_secret": self.secret_key,
        }
        self._http = SyncClient(
            base_url=BASE_URL,
            timeout=self.timeout,
            follow_redirects=True,
        )

    def __enter__(self) -> "SyncQvaPayMerchant":
        return self

    def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self._http.aclose()

    def info(self) -> App:
        """Get app info."""
        response = self._http.post("info", json=self._auth)
        validate_response(response)
        return App.from_json(response.json())

    def balance(self) -> float:
        """Get app owner balance."""
        response = self._http.post("balance", json=self._auth)
        validate_response(response)
        return float(response.json())

    def create_invoice(
        self,
        amount: float,
        description: str,
        remote_id: str,
        signed: bool = False,
    ) -> Invoice:
        """Create an invoice."""
        body = {
            **self._auth,
            "amount": amount,
            "description": description,
            "remote_id": remote_id,
            "signed": int(signed),
        }
        response = self._http.post("create_invoice", json=body)
        validate_response(response)
        return Invoice.from_json(response.json())

    def modify_invoice(self, uuid: str, **kwargs: Any) -> Invoice:
        """Modify an existing invoice."""
        body = {**self._auth, "uuid": uuid, **kwargs}
        response = self._http.post("modify_invoice", json=body)
        validate_response(response)
        return Invoice.from_json(response.json())

    def get_transactions(self) -> PaginatedTransactions:
        """Get app transactions."""
        response = self._http.post("transactions", json=self._auth)
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    def get_transaction_status(self, uuid: str) -> Any:
        """Get transaction status."""
        body = {**self._auth, "uuid": uuid}
        response = self._http.post("transaction_status", json=body)
        validate_response(response)
        return response.json()

    def get_payments_authorization(self, **kwargs: Any) -> Any:
        """Get payments authorization."""
        body = {**self._auth, **kwargs}
        response = self._http.post("payments_authorization", json=body)
        validate_response(response)
        return response.json()

    def charge_user(self, **kwargs: Any) -> Any:
        """Charge a user with an authorized token."""
        body = {**self._auth, **kwargs}
        response = self._http.post("charge_user", json=body)
        validate_response(response)
        return response.json()
