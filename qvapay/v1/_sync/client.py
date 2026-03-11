from dataclasses import dataclass, field
from typing import Union
from uuid import UUID

from ..auth import QvaPayAuth
from ..http_clients import DEFAULT_TIMEOUT, SyncClient, TimeoutTypes
from ..models.info import Info
from ..models.invoice import Invoice
from ..models.paginated_transactions import PaginatedTransactions
from ..models.transaction_detail import TransactionDetail
from ..utils import validate_response


@dataclass
class SyncQvaPayClient:
    """
    Creates a QvaPay merchant client.
    * uuid: QvaPay app UUID.
    * secret_key: QvaPay app secret key.
    Get your app credentials at: https://qvapay.com/apps/create
    """

    uuid: str
    secret_key: str
    timeout: TimeoutTypes = field(default_factory=lambda: DEFAULT_TIMEOUT)

    def __post_init__(self):
        self.auth_body = {
            "uuid": self.uuid,
            "secret_key": self.secret_key,
        }
        self.base_url = "https://api.qvapay.com/v2"
        self.http_client = SyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            follow_redirects=True,
        )

    def __enter__(self) -> "SyncQvaPayClient":
        return self

    def __exit__(self, exc_t, exc_v, exc_tb) -> None:
        self.close()

    def close(self) -> None:
        self.http_client.aclose()

    @staticmethod
    def from_auth(
        auth: QvaPayAuth,
        timeout: TimeoutTypes = DEFAULT_TIMEOUT,
    ) -> "SyncQvaPayClient":
        return SyncQvaPayClient(auth.uuid, auth.secret_key, timeout)

    def get_info(self) -> Info:
        """
        Get info relating to your QvaPay app.
        https://qvapay.com/docs/1.0/app_info
        """
        response = self.http_client.post("info", json=self.auth_body)
        validate_response(response)
        return Info.from_json(response.json())

    def get_balance(self) -> float:
        """
        Get your QvaPay balance.
        https://qvapay.com/docs/1.0/balance
        """
        response = self.http_client.post("balance", json=self.auth_body)
        validate_response(response)
        return float(response.json())

    def get_transactions(self, page: int = 1) -> PaginatedTransactions:
        """
        Gets transactions list, paginated by 50 items per request.
        * page: Page to be fetched.
        https://qvapay.com/docs/1.0/transactions
        """
        body = {**self.auth_body, "page": page}
        response = self.http_client.post("transactions", json=body)
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    def get_transaction(self, id: Union[str, UUID]) -> TransactionDetail:
        """
        Gets a transaction by its id (uuid).
        * id: Transaction uuid returned by QvaPay when created.
        https://qvapay.com/docs/1.0/transaction
        """
        response = self.http_client.post(f"transactions/{id}", json=self.auth_body)
        validate_response(response)
        return TransactionDetail.from_json(response.json())

    def create_invoice(
        self,
        amount: float,
        description: str,
        remote_id: str,
        signed: bool = False,
    ) -> Invoice:
        """
        Creates an invoice.
        * amount: Amount of money to receive to your wallet, expressed in
          dollars with two decimals.
        * description: Description of the invoice to be created, useful to
          show info to the user who pays. Max 300 chars.
        * remote_id: Invoice ID on your side (example: in your e-commerce
          store). Optional.
        * signed: Generates a signed URL, valid for 30 minutes. Useful to
          increase security, introducing an expiration datetime. Optional.
        https://qvapay.com/docs/1.0/create_invoice
        """
        body = {
            **self.auth_body,
            "amount": amount,
            "description": description,
            "remote_id": remote_id,
            "signed": int(signed),
        }
        response = self.http_client.post("create_invoice", json=body)
        validate_response(response)
        return Invoice.from_json(response.json())
