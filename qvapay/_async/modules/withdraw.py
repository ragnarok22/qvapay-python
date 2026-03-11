from typing import Any, Dict, List, Optional

from httpx import AsyncClient

from ...models.withdrawal import Withdrawal
from ...utils import validate_response


class WithdrawModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def create(
        self,
        pay_method: str,
        amount: float,
        details: Dict[str, str],
        *,
        pin: Optional[int] = None,
        note: str = "",
    ) -> Withdrawal:
        """Withdraw funds to an available destination.

        Args:
            pay_method: Payment method (e.g. ``"USDT"``, ``"BTCLN"``,
                ``"BANK_MLC"``, ``"USDCASH"``).
            amount: Amount to withdraw.
            details: Destination details. The required keys depend on the
                payment method (e.g. ``{"Wallet": "..."}`` for crypto,
                or bank/personal info for fiat).
            pin: Security PIN. Can be omitted when the wallet is already
                configured in your payment methods.
            note: Personal notes for recognizing the withdrawal in records.
        """
        payload: Dict[str, Any] = {
            "pay_method": pay_method,
            "amount": amount,
            "details": details,
        }
        if pin is not None:
            payload["pin"] = pin
        if note:
            payload["note"] = note
        response = await self._http.post("withdraw", json=payload)
        validate_response(response)
        return Withdrawal.from_json(response.json())

    async def list(self) -> List[Withdrawal]:
        """Get the last 10 withdrawals for the authenticated user."""
        response = await self._http.get("withdraws")
        validate_response(response)
        return [Withdrawal.from_json(w) for w in response.json()["data"]]

    async def get(self, uuid: str) -> Withdrawal:
        """Get withdrawal details."""
        response = await self._http.get(f"withdraw/{uuid}")
        validate_response(response)
        return Withdrawal.from_json(response.json())

    async def balance(self) -> Any:
        """Withdraw balance."""
        response = await self._http.post("withdraw/balance")
        validate_response(response)
        return response.json()
