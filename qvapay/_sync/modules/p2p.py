from typing import Any, List

from httpx import Client

from ...models.p2p import P2PMessage, P2POffer
from ...utils import validate_response


class ChatSubModule:
    def __init__(self, http: Client):
        self._http = http

    def get(self, offer_uuid: str) -> List[P2PMessage]:
        """Get P2P chat messages for an offer."""
        response = self._http.get(f"p2p/{offer_uuid}/chat")
        validate_response(response)
        return [P2PMessage.from_json(m) for m in response.json()]

    def send(
        self, offer_uuid: str, message: str
    ) -> P2PMessage:
        """Send a message in P2P chat."""
        response = self._http.post(
            f"p2p/{offer_uuid}/chat",
            json={"message": message},
        )
        validate_response(response)
        return P2PMessage.from_json(response.json())


class P2PModule:
    def __init__(self, http: Client):
        self._http = http
        self.chat = ChatSubModule(http)

    def average(self, coin: str) -> Any:
        """Get P2P average for a coin."""
        response = self._http.get(
            "p2p/average", params={"coin": coin}
        )
        validate_response(response)
        return response.json()

    def averages(self) -> Any:
        """Get all P2P averages."""
        response = self._http.get("p2p/averages")
        validate_response(response)
        return response.json()

    def completed_pairs_average(self, coin: str) -> float:
        """Get completed trading pairs average."""
        response = self._http.get(
            "p2p/completed_pairs_average",
            params={"coin": coin.upper()},
        )
        validate_response(response)
        return float(response.text)

    def total_public_open_ops(self) -> Any:
        """Get total public open operations."""
        response = self._http.get("p2p/total_public_open_ops")
        validate_response(response)
        return response.json()

    def get_offers(self) -> List[P2POffer]:
        """Get all P2P offers."""
        response = self._http.get("p2p")
        validate_response(response)
        return [P2POffer.from_json(o) for o in response.json()]

    def get_my_offers(self) -> List[P2POffer]:
        """Get my P2P offers."""
        response = self._http.get("p2p/my")
        validate_response(response)
        return [P2POffer.from_json(o) for o in response.json()]

    def get_offer(self, uuid: str) -> P2POffer:
        """Get a specific P2P offer."""
        response = self._http.get(f"p2p/{uuid}")
        validate_response(response)
        return P2POffer.from_json(response.json())

    def get_offer_public(self, uuid: str) -> P2POffer:
        """Get public data of a P2P offer."""
        response = self._http.get(f"p2p/{uuid}/public")
        validate_response(response)
        return P2POffer.from_json(response.json())

    def create_offer(self, **kwargs: Any) -> P2POffer:
        """Create a new P2P offer."""
        response = self._http.post("p2p", json=kwargs)
        validate_response(response)
        return P2POffer.from_json(response.json())

    def edit_offer(self, uuid: str, **kwargs: Any) -> P2POffer:
        """Edit a P2P offer."""
        response = self._http.post(
            f"p2p/{uuid}/edit", json=kwargs
        )
        validate_response(response)
        return P2POffer.from_json(response.json())

    def apply(self, uuid: str) -> Any:
        """Apply to a P2P offer."""
        response = self._http.post(f"p2p/{uuid}/apply")
        validate_response(response)
        return response.json()

    def mark_paid(self, uuid: str) -> Any:
        """Mark a P2P offer as paid."""
        response = self._http.post(f"p2p/{uuid}/mark_paid")
        validate_response(response)
        return response.json()

    def confirm_received(self, uuid: str) -> Any:
        """Confirm received for a P2P offer."""
        response = self._http.post(
            f"p2p/{uuid}/confirm_received"
        )
        validate_response(response)
        return response.json()

    def cancel(self, uuid: str) -> Any:
        """Cancel a P2P offer."""
        response = self._http.post(f"p2p/{uuid}/cancel")
        validate_response(response)
        return response.json()

    def rate(self, uuid: str, rating: int) -> Any:
        """Rate a P2P offer."""
        response = self._http.post(
            f"p2p/{uuid}/rate", json={"rating": rating}
        )
        validate_response(response)
        return response.json()
