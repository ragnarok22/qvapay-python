from typing import Any, List

from httpx import AsyncClient

from ...models.p2p import P2PMessage, P2POffer
from ...utils import validate_response


class ChatSubModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def get(self, offer_uuid: str) -> List[P2PMessage]:
        """Get P2P chat messages for an offer."""
        response = await self._http.get(f"p2p/{offer_uuid}/chat")
        validate_response(response)
        return [P2PMessage.from_json(m) for m in response.json()]

    async def send(self, offer_uuid: str, message: str) -> P2PMessage:
        """Send a message in P2P chat."""
        response = await self._http.post(
            f"p2p/{offer_uuid}/chat",
            json={"message": message},
        )
        validate_response(response)
        return P2PMessage.from_json(response.json())


class P2PModule:
    def __init__(self, http: AsyncClient):
        self._http = http
        self.chat = ChatSubModule(http)

    async def average(self, coin: str) -> Any:
        """Get P2P average for a coin."""
        response = await self._http.get("p2p/average", params={"coin": coin})
        validate_response(response)
        return response.json()

    async def averages(self) -> Any:
        """Get all P2P averages."""
        response = await self._http.get("p2p/averages")
        validate_response(response)
        return response.json()

    async def completed_pairs_average(self, coin: str) -> float:
        """Get completed trading pairs average."""
        response = await self._http.get(
            "p2p/completed_pairs_average",
            params={"coin": coin.upper()},
        )
        validate_response(response)
        return float(response.text)

    async def total_public_open_ops(self) -> Any:
        """Get total public open operations."""
        response = await self._http.get("p2p/total_public_open_ops")
        validate_response(response)
        return response.json()

    async def get_offers(self) -> List[P2POffer]:
        """Get all P2P offers."""
        response = await self._http.get("p2p")
        validate_response(response)
        return [P2POffer.from_json(o) for o in response.json()]

    async def get_my_offers(self) -> List[P2POffer]:
        """Get my P2P offers."""
        response = await self._http.get("p2p/my")
        validate_response(response)
        return [P2POffer.from_json(o) for o in response.json()]

    async def get_offer(self, uuid: str) -> P2POffer:
        """Get a specific P2P offer."""
        response = await self._http.get(f"p2p/{uuid}")
        validate_response(response)
        return P2POffer.from_json(response.json())

    async def get_offer_public(self, uuid: str) -> P2POffer:
        """Get public data of a P2P offer."""
        response = await self._http.get(f"p2p/{uuid}/public")
        validate_response(response)
        return P2POffer.from_json(response.json())

    async def create_offer(self, **kwargs: Any) -> P2POffer:
        """Create a new P2P offer."""
        response = await self._http.post("p2p", json=kwargs)
        validate_response(response)
        return P2POffer.from_json(response.json())

    async def edit_offer(self, uuid: str, **kwargs: Any) -> P2POffer:
        """Edit a P2P offer."""
        response = await self._http.post(f"p2p/{uuid}/edit", json=kwargs)
        validate_response(response)
        return P2POffer.from_json(response.json())

    async def apply(self, uuid: str) -> Any:
        """Apply to a P2P offer."""
        response = await self._http.post(f"p2p/{uuid}/apply")
        validate_response(response)
        return response.json()

    async def mark_paid(self, uuid: str) -> Any:
        """Mark a P2P offer as paid."""
        response = await self._http.post(f"p2p/{uuid}/mark_paid")
        validate_response(response)
        return response.json()

    async def confirm_received(self, uuid: str) -> Any:
        """Confirm received for a P2P offer."""
        response = await self._http.post(f"p2p/{uuid}/confirm_received")
        validate_response(response)
        return response.json()

    async def cancel(self, uuid: str) -> Any:
        """Cancel a P2P offer."""
        response = await self._http.post(f"p2p/{uuid}/cancel")
        validate_response(response)
        return response.json()

    async def rate(self, uuid: str, rating: int) -> Any:
        """Rate a P2P offer."""
        response = await self._http.post(f"p2p/{uuid}/rate", json={"rating": rating})
        validate_response(response)
        return response.json()
