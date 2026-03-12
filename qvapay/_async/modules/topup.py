from typing import Any, List

from httpx import AsyncClient

from ...utils import validate_response


class TopupModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list_products(self) -> List[Any]:
        """List available phone top-up packages."""
        response = await self._http.get("store/phone_package")
        validate_response(response)
        payload = response.json()
        if isinstance(payload, dict) and isinstance(
            payload.get("phone_packages"), list
        ):
            return payload["phone_packages"]
        return payload
