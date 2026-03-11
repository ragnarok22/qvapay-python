from typing import List

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
        return [PaymentLink.from_json(item) for item in response.json()]

    def create(self, name: str, product_id: str, amount: float) -> PaymentLink:
        """Create a payment link."""
        payload = {
            "name": name,
            "product_id": product_id,
            "amount": amount,
        }
        response = self._http.post("payment_links/create", json=payload)
        validate_response(response)
        return PaymentLink.from_json(response.json())
