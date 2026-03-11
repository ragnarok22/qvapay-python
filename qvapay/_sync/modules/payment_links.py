from typing import Any, List

from httpx import Client

from ...models.payment_link import PaymentLink
from ...utils import validate_response


class PaymentLinksModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> List[PaymentLink]:
        """Get payment links."""
        response = self._http.get("payment_links")
        validate_response(response)
        return [PaymentLink.from_json(l) for l in response.json()]

    def create(
        self, amount: float, description: str, **kwargs: Any
    ) -> PaymentLink:
        """Create a payment link."""
        payload = {
            "amount": amount,
            "description": description,
            **kwargs,
        }
        response = self._http.post(
            "payment_links", json=payload
        )
        validate_response(response)
        return PaymentLink.from_json(response.json())
