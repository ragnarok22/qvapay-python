from typing import Any, List

from httpx import Client

from ...models.withdrawal import Withdrawal
from ...utils import validate_response


class WithdrawModule:
    def __init__(self, http: Client):
        self._http = http

    def create(self, pay_method: str, amount: float, **kwargs: Any) -> Withdrawal:
        """Request a withdrawal."""
        payload = {"pay_method": pay_method, "amount": amount, **kwargs}
        response = self._http.post("withdraw", json=payload)
        validate_response(response)
        return Withdrawal.from_json(response.json())

    def list(self) -> List[Withdrawal]:
        """Get withdrawal history."""
        response = self._http.get("withdraw")
        validate_response(response)
        return [Withdrawal.from_json(w) for w in response.json()]

    def get(self, uuid: str) -> Withdrawal:
        """Get withdrawal details."""
        response = self._http.get(f"withdraw/{uuid}")
        validate_response(response)
        return Withdrawal.from_json(response.json())

    def balance(self) -> Any:
        """Withdraw balance."""
        response = self._http.post("withdraw/balance")
        validate_response(response)
        return response.json()
