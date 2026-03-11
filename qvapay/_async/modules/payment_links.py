from typing import Any, List

from httpx import AsyncClient

from ...models.payment_link import PaymentLink
from ...utils import validate_response


class PaymentLinksModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> List[PaymentLink]:
        """Get payment links."""
        response = await self._http.get("payment_links")
        validate_response(response)
        return [PaymentLink.from_json(item) for item in response.json()]

    async def create(
        self, amount: float, description: str, **kwargs: Any
    ) -> PaymentLink:
        """Create a payment link."""
        payload = {
            "amount": amount,
            "description": description,
            **kwargs,
        }
        response = await self._http.post("payment_links", json=payload)
        validate_response(response)
        return PaymentLink.from_json(response.json())
