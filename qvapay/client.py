from __future__ import absolute_import

from dataclasses import dataclass, field

import httpx

from .errors import QvaPayError
from .models.info import Info
from .models.invoice import Invoice
from .models.transaction import PaginatedTransactions, TransactionDetail


def validate_response(response: httpx.Response) -> None:
    if response.status_code != 200:
        raise QvaPayError(response.status_code)


@dataclass
class Client:
    """
    Creates a QvaPay client.
    * app_id: QvaPay app id.
    * app_secret: QvaPay app secret.
    Get your app credentials at: https://qvapay.com/apps/create
    """

    app_id: str
    app_secret: str
    version: int = 1
    request: httpx.Client = field(init=False)

    def __post_init__(self):
        self.request = httpx.Client(
            base_url=f"https://qvapay.com/api/v{self.version}",
            params={"app_id": self.app_id, "app_secret": self.app_secret},
        )

    def info(self) -> Info:
        """
        Get info relating to your QvaPay app.
        https://qvapay.com/docs/2.0/app_info
        """
        response = self.request.get("info")
        validate_response(response)
        return Info.from_dict(response.json())

    def balance(self) -> dict:
        """
        Get your QvaPay balance.
        https://qvapay.com/docs/2.0/balance
        """
        # with self.request as request:
        response = self.request.get("balance")
        validate_response(response)
        return response.json()

    def transactions(self, page: int = 1) -> PaginatedTransactions:
        """
        Gets transactions list, paginated by 50 items per request.
        * page: Page to be fetched.
        https://qvapay.com/docs/2.0/transactions
        """
        params = {"page": str(page)}
        response = self.request.get("transactions", params=params)
        validate_response(response)
        return PaginatedTransactions.from_dict(response.json())

    def get_transaction(self, id: str) -> TransactionDetail:
        """
        Gets a transaction by its id (uuid).
        * id: Transaction uuid returned by QvaPay when created.
        https://qvapay.com/docs/2.0/transaction
        """
        response = self.request.get(f"transaction/{id}")
        validate_response(response)
        return TransactionDetail.from_dict(response.json())

    def create_invoice(
        self,
        amount: float,
        description: str,
        remote_id: str,
        signed: bool = False,
    ) -> Invoice:
        """
        Creates an invoice.
        * amount: Amount of money to receive to your wallet, expressed in dollars with two decimals.
        * description: Description of the invoice to be created, useful to show info to the user who pays. Max 300 chars.
        * remote_id: Invoice ID on your side (example: in your e-commerce store). Optional.
        * signed: Generates a signed URL, valid for 30 minutes. Useful to increase security, introducing an expiration datetime. Optional.
        https://qvapay.com/docs/2.0/create_invoice
        """
        params = {
            "amount": amount,
            "description": description,
            "remote_id": remote_id,
            "signed": 1 if signed else 0,
        }
        response = self.request.get("create_invoice", params=params)
        validate_response(response)
        return Invoice.from_dict(response.json())
