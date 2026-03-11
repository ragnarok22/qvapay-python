from typing import Any, List

from httpx import AsyncClient

from ...models.withdrawal import Withdrawal
from ...utils import validate_response


class WithdrawModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def create(
        self, pay_method: str, amount: float, **kwargs: Any
    ) -> Withdrawal:
        """Request a withdrawal."""
        payload = {"pay_method": pay_method, "amount": amount, **kwargs}
        response = await self._http.post("withdraw", json=payload)
        validate_response(response)
        return Withdrawal.from_json(response.json())

    async def list(self) -> List[Withdrawal]:
        """Get withdrawal history."""
        response = await self._http.get("withdraw")
        validate_response(response)
        return [Withdrawal.from_json(w) for w in response.json()]

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
