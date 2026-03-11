from typing import Any, List

from httpx import Client

from ...models.transaction import (
    PaginatedTransactions,
    Transaction,
    TransactionDetail,
)
from ...utils import validate_response


class TransactionsModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> PaginatedTransactions:
        """Get transactions list."""
        response = self._http.get("transactions")
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    def sent_to_user(self) -> List[Transaction]:
        """Get transactions sent to user."""
        response = self._http.get("transactions/sent")
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    def latest_sent(self) -> List[Transaction]:
        """Get latest users sent transactions."""
        response = self._http.get("transactions/latest_sent")
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    def get(self, uuid: str) -> TransactionDetail:
        """Get a transaction by UUID."""
        response = self._http.get(f"transactions/{uuid}")
        validate_response(response)
        return TransactionDetail.from_json(response.json())

    def get_pdf(self, uuid: str) -> bytes:
        """Get a transaction details as PDF."""
        response = self._http.get(f"transactions/{uuid}/pdf")
        validate_response(response)
        return response.content

    def transfer(self, to: str, amount: float, description: str = "") -> Any:
        """Transfer balance to another user."""
        payload = {
            "to": to,
            "amount": amount,
            "description": description,
        }
        response = self._http.post("transactions/transfer", json=payload)
        validate_response(response)
        return response.json()

    def transfer_app(self, **kwargs: Any) -> Any:
        """Transfer balance via app."""
        response = self._http.post("transactions/transfer_app", json=kwargs)
        validate_response(response)
        return response.json()

    def pay(self, uuid: str, pin: str) -> Any:
        """Pay a transaction."""
        payload = {"uuid": uuid, "pin": pin}
        response = self._http.post("transactions/pay", json=payload)
        validate_response(response)
        return response.json()
