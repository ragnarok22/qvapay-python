from typing import Any, List, Optional

from httpx import AsyncClient

from ...models.transaction import (
    PaginatedTransactions,
    Transaction,
    TransactionDetail,
)
from ...utils import validate_response


class TransactionsModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> PaginatedTransactions:
        """Get transactions list."""
        response = await self._http.get("transactions")
        validate_response(response)
        return PaginatedTransactions.from_json(response.json())

    async def sent_to_user(self) -> List[Transaction]:
        """Get transactions sent to user."""
        response = await self._http.get("transactions/sent")
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    async def latest_sent(self) -> List[Transaction]:
        """Get latest users sent transactions."""
        response = await self._http.get("transactions/latest_sent")
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    async def get(self, uuid: str) -> TransactionDetail:
        """Get a transaction by UUID."""
        response = await self._http.get(f"transactions/{uuid}")
        validate_response(response)
        return TransactionDetail.from_json(response.json())

    async def get_pdf(self, uuid: str) -> bytes:
        """Get a transaction details as PDF."""
        response = await self._http.get(f"transactions/{uuid}/pdf")
        validate_response(response)
        return response.content

    async def transfer(
        self, to: str, amount: float, description: str = ""
    ) -> Any:
        """Transfer balance to another user."""
        payload = {
            "to": to,
            "amount": amount,
            "description": description,
        }
        response = await self._http.post(
            "transactions/transfer", json=payload
        )
        validate_response(response)
        return response.json()

    async def transfer_app(self, **kwargs: Any) -> Any:
        """Transfer balance via app."""
        response = await self._http.post(
            "transactions/transfer_app", json=kwargs
        )
        validate_response(response)
        return response.json()

    async def pay(self, uuid: str, pin: str) -> Any:
        """Pay a transaction."""
        payload = {"uuid": uuid, "pin": pin}
        response = await self._http.post(
            "transactions/pay", json=payload
        )
        validate_response(response)
        return response.json()
