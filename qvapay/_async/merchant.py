from dataclasses import dataclass, field
from typing import Any

from ..http import DEFAULT_TIMEOUT, V2_BASE_URL, AsyncClient, TimeoutTypes
from ..models.app import App
from ..models.invoice import Invoice
from ..models.transaction import PaginatedTransactions
from ..utils import validate_response


@dataclass
class AsyncQvaPayMerchant:
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
        self._http = AsyncClient(
            base_url=V2_BASE_URL,
            timeout=self.timeout,
            follow_redirects=True,
        )

    async def __aenter__(self) -> "AsyncQvaPayMerchant":
        return self

    async def __aexit__(self, exc_t, exc_v, exc_tb) -> None:
        await self.close()

    async def close(self) -> None:
        await self._http.aclose()

    async def info(self) -> App:
        """Get app info."""
        response = await self._http.post("info", json=self._auth)
        validate_response(response)
        return App.from_json(response.json())

    async def balance(self) -> float:
        """Get app owner balance."""
        response = await self._http.post("balance", json=self._auth)
        validate_response(response)
        return float(response.json())

    async def create_invoice(
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
        response = await self._http.post("create_invoice", json=body)
        validate_response(response)
        return Invoice.from_json(response.json())

    async def modify_invoice(self, uuid: str, **kwargs: Any) -> Invoice:
        """Modify an existing invoice."""
        body = {**self._auth, "uuid": uuid, **kwargs}
        response = await self._http.post("modify_invoice", json=body)
        validate_response(response)
        return Invoice.from_json(response.json())

    async def get_transactions(self) -> PaginatedTransactions:
        """Get app transactions."""
        response = await self._http.post("transactions", json=self._auth)
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    async def get_transaction_status(self, uuid: str) -> Any:
        """Get transaction status by UUID."""
        body = {**self._auth, "uuid": uuid}
        response = await self._http.post(f"transactions/{uuid}", json=body)
        validate_response(response)
        return response.json()

    async def get_payments_authorization(self, **kwargs: Any) -> Any:
        """Get payments authorization URL."""
        body = {**self._auth, **kwargs}
        response = await self._http.post("authorize_payments", json=body)
        validate_response(response)
        return response.json()

    async def charge_user(self, **kwargs: Any) -> Any:
        """Charge a user with an authorized token."""
        body = {**self._auth, **kwargs}
        response = await self._http.post("charge", json=body)
        validate_response(response)
        return response.json()
