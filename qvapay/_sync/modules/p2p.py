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

    def send(self, offer_uuid: str, message: str) -> P2PMessage:
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

    @staticmethod
    def _normalize_params(**kwargs: Any) -> dict[str, Any]:
        params: dict[str, Any] = {}
        for key, value in kwargs.items():
            if value is None:
                continue
            if isinstance(value, bool):
                params[key] = str(value).lower()
            else:
                params[key] = value
        return params

    @staticmethod
    def _offer_items(payload: Any) -> list[Any]:
        if isinstance(payload, dict) and isinstance(payload.get("data"), list):
            return payload["data"]
        return payload

    def average(self, coin: str) -> Any:
        """Get P2P average for a coin."""
        response = self._http.get("p2p/average", params={"coin": coin})
        validate_response(response)
        return response.json()

    def averages(self) -> Any:
        """Get all P2P averages."""
        response = self._http.get("p2p/averages")
        validate_response(response)
        return response.json()

    def completed_pairs_average(self, coin: str) -> Any:
        """Get aggregate stats for completed trading pairs."""
        response = self._http.get(
            "p2p/completed_pairs_average",
            params={"coin": coin.upper()},
        )
        validate_response(response)
        return response.json()

    def total_public_open_ops(self) -> Any:
        """Get total public open operations."""
        response = self._http.get("p2p/get_total_operations")
        validate_response(response)
        return response.json()

    def get_offers(self, **filters: Any) -> List[P2POffer]:
        """Get all P2P offers."""
        response = self._http.get(
            "p2p",
            params=self._normalize_params(**filters),
        )
        validate_response(response)
        return [P2POffer.from_json(o) for o in self._offer_items(response.json())]

    def get_my_offers(self, **filters: Any) -> List[P2POffer]:
        """Get my P2P offers."""
        response = self._http.get(
            "p2p",
            params=self._normalize_params(my=True, **filters),
        )
        validate_response(response)
        return [P2POffer.from_json(o) for o in self._offer_items(response.json())]

    def get_offer(self, uuid: str) -> P2POffer:
        """Get a specific P2P offer."""
        response = self._http.get(f"p2p/{uuid}")
        validate_response(response)
        return P2POffer.from_json(response.json())

    def get_offer_public(self, uuid: str) -> P2POffer:
        """Get public data of a P2P offer."""
        response = self._http.get(f"p2p/{uuid}/pub")
        validate_response(response)
        return P2POffer.from_json(response.json())

    def create_offer(self, **kwargs: Any) -> P2POffer:
        """Create a new P2P offer."""
        response = self._http.post("p2p/create", json=kwargs)
        validate_response(response)
        return P2POffer.from_json(response.json())

    def edit_offer(self, uuid: str, **kwargs: Any) -> P2POffer:
        """Edit a P2P offer."""
        response = self._http.post(f"p2p/{uuid}/edit", json=kwargs)
        validate_response(response)
        return P2POffer.from_json(response.json())

    def apply(self, uuid: str) -> Any:
        """Apply to a P2P offer."""
        response = self._http.post(f"p2p/{uuid}/apply")
        validate_response(response)
        return response.json()

    def mark_paid(self, uuid: str) -> Any:
        """Mark a P2P offer as paid."""
        response = self._http.post(f"p2p/{uuid}/paid")
        validate_response(response)
        return response.json()

    def confirm_received(self, uuid: str) -> Any:
        """Confirm received for a P2P offer."""
        response = self._http.post(f"p2p/{uuid}/received")
        validate_response(response)
        return response.json()

    def cancel(self, uuid: str) -> Any:
        """Cancel a P2P offer."""
        response = self._http.post(f"p2p/{uuid}/cancel")
        validate_response(response)
        return response.json()

    def rate(self, uuid: str, rating: int) -> Any:
        """Rate a P2P offer."""
        response = self._http.post(f"p2p/{uuid}/rate", json={"rating": rating})
        validate_response(response)
        return response.json()
