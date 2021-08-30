from __future__ import absolute_import

import httpx

from qvapay.errors import QvaPayError
from qvapay.models.info import Info
from qvapay.models.invoice import Invoice
from qvapay.models.transaction import (
    PaginatedTransactions,
    Transaction,
    TransactionDetail,
)


def validate_response(response: httpx.Response) -> None:
    if response.status_code != 200:
        raise QvaPayError(response.status_code)


class Client(object):
    app_id = None
    app_secret = None
    version = None

    data = None

    def __init__(self, app_id, app_secret, version=1):
        """
        Creates a QvaPay client.
        * app_id: QvaPay app id.
        * app_secret: QvaPay app secret.
        Get your app credentials at: https://qvapay.com/apps/create
        """
        self.app_id = app_id
        self.app_secret = app_secret
        self.version = version
        self.request = httpx.Client(
            base_url=f"https://stage.qvapay.com/api/v{self.version}",
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

    def get_transaction(self, id: str):
        """
        Gets a transaction by its id (uuid).
        * id: Transaction uuid returned by QvaPay when created.
        https://qvapay.com/docs/2.0/transaction
        """
        response = self.request.get(f"transactions/{id}")
        validate_response(response)
        return TransactionDetail.from_dict(response.json())
