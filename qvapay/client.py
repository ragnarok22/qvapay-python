from __future__ import absolute_import

import httpx

from qvapay.errors import QvaPayError
from qvapay.resources.info import Info
from qvapay.resources.invoice import Invoice
from qvapay.resources.transaction import PaginatedTransactions, Transaction


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
        return Info(**response.json())

    def balance(self) -> dict:
        """
        Get your QvaPay balance.
        https://qvapay.com/docs/2.0/balance
        """
        # with self.request as request:
        response = self.request.get("balance")
        validate_response(response)
        return response.json()
