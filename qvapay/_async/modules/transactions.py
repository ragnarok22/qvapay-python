from typing import Dict, List, Optional

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
        response = await self._http.get("transaction", params=params)
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    async def sent_to_user(
        self,
        user_uuid: str,
        *,
        take: Optional[int] = None,
        start: Optional[str] = None,
        end: Optional[str] = None,
        status: Optional[str] = None,
        remote_id: Optional[str] = None,
        description: Optional[str] = None,
    ) -> List[Transaction]:
        """Get transactions sent to a specific user.

        Args:
            user_uuid: UUID of the recipient user.
            take: Number of results to return.
        """
        params = self._build_params(
            start=start,
            end=end,
            status=status,
            remote_id=remote_id,
            description=description,
        )
        params["user_uuid"] = user_uuid
        if take is not None:
            params["take"] = str(take)
        response = await self._http.get("transaction", params=params)
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    async def latest_sent(self) -> List[Transaction]:
        """Get latest users sent transactions."""
        response = await self._http.get("transaction/latestusers")
        validate_response(response)
        return [Transaction.from_json(t) for t in response.json()]

    async def get(self, uuid: str) -> TransactionDetail:
        """Get a transaction by UUID."""
        response = await self._http.get(f"transaction/{uuid}")
        validate_response(response)
        return TransactionDetail.from_json(response.json())

    async def get_pdf(self, uuid: str) -> bytes:
        """Get a transaction details as PDF."""
        response = await self._http.get(f"transaction/{uuid}/pdf")
        validate_response(response)
        return response.content

    async def transfer(
        self,
        to: str,
        amount: float,
        description: str = "",
        pin: Optional[str] = None,
    ) -> Transaction:
        """Transfer balance to another user.

        The ``to`` field accepts a user UUID, email, or phone number.

        Args:
            to: Destination user UUID, email, or phone.
            amount: Amount to transfer.
            description: Optional transfer description.
        """
        payload = {
            "to": to,
            "amount": amount,
            "description": description,
        }
        if pin is not None:
            payload["pin"] = pin
        response = await self._http.post("transaction/transfer", json=payload)
        validate_response(response)
        return Transaction.from_json(response.json())

    async def transfer_app(
        self,
        to: str,
        amount: float,
        description: str = "",
        pin: Optional[str] = None,
    ) -> Transaction:
        """Transfer balance via app.

        The ``to`` field accepts a user UUID, email, or phone number.

        Args:
            to: Destination user UUID, email, or phone.
            amount: Amount to transfer.
            description: Optional transfer description.
        """
        payload = {
            "to": to,
            "amount": amount,
            "description": description,
        }
        if pin is not None:
            payload["pin"] = pin
        response = await self._http.post("transaction/transfer", json=payload)
        validate_response(response)
        return Transaction.from_json(response.json())

    async def pay(self, uuid: str, pin: str) -> Transaction:
        """Pay a pending transaction.

        Args:
            uuid: UUID of the transaction to pay.
            pin: User's PIN (default is "0000").
        """
        payload = {"uuid": uuid, "pin": pin}
        response = await self._http.post(f"transaction/{uuid}/pay", json=payload)
        validate_response(response)
        return Transaction.from_json(response.json())
