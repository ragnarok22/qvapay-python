from typing import Any, Dict, List, Optional

from httpx import AsyncClient

from ...models.transaction import (
    Transaction,
    TransactionDetail,
)
from ...utils import validate_response


class TransactionsModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    @staticmethod
    def _build_params(
        *,
        start: Optional[str] = None,
        end: Optional[str] = None,
        status: Optional[str] = None,
        remote_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, str]:
        params: Dict[str, str] = {}
        if start is not None:
            params["start"] = start
        if end is not None:
            params["end"] = end
        if status is not None:
            params["status"] = status
        if remote_id is not None:
            params["remote_id"] = remote_id
        if description is not None:
            params["description"] = description
        return params

    async def list(
        self,
        *,
        start: Optional[str] = None,
        end: Optional[str] = None,
        status: Optional[str] = None,
        remote_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> List[Transaction]:
        """Get transactions list.

        Returns the last 30 transactions for the authenticated user.
        Results can be filtered by the following parameters:

        Args:
            start: Filter by start datetime (e.g. "2021-10-17 13:05:30").
            end: Filter by end datetime (e.g. "2021-10-17 13:10:10").
            status: Filter by status ("paid", "pending", or "cancelled").
            remote_id: Filter by remote_id.
            description: Filter by description text.
        """
        params = self._build_params(
            start=start,
            end=end,
            status=status,
            remote_id=remote_id,
            description=description,
        )
        response = await self._http.get("transactions", params=params)
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    async def sent_to_user(
        self,
        *,
        start: Optional[str] = None,
        end: Optional[str] = None,
        status: Optional[str] = None,
        remote_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> List[Transaction]:
        """Get transactions sent to user."""
        params = self._build_params(
            start=start,
            end=end,
            status=status,
            remote_id=remote_id,
            description=description,
        )
        response = await self._http.get("transactions/sent", params=params)
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    async def latest_sent(
        self,
        *,
        start: Optional[str] = None,
        end: Optional[str] = None,
        status: Optional[str] = None,
        remote_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> List[Transaction]:
        """Get latest users sent transactions."""
        params = self._build_params(
            start=start,
            end=end,
            status=status,
            remote_id=remote_id,
            description=description,
        )
        response = await self._http.get("transactions/latest_sent", params=params)
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

    async def transfer(self, to: str, amount: float, description: str = "") -> Any:
        """Transfer balance to another user."""
        payload = {
            "to": to,
            "amount": amount,
            "description": description,
        }
        response = await self._http.post("transactions/transfer", json=payload)
        validate_response(response)
        return response.json()

    async def transfer_app(self, **kwargs: Any) -> Any:
        """Transfer balance via app."""
        response = await self._http.post("transactions/transfer_app", json=kwargs)
        validate_response(response)
        return response.json()

    async def pay(self, uuid: str, pin: str) -> Any:
        """Pay a transaction."""
        payload = {"uuid": uuid, "pin": pin}
        response = await self._http.post("transactions/pay", json=payload)
        validate_response(response)
        return response.json()
