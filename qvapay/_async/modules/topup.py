from typing import Any, List

from httpx import AsyncClient

from ...utils import validate_response


class TopupModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list_products(self) -> List[Any]:
        """List available phone top-up products."""
        response = await self._http.get("topup/products")
        validate_response(response)
        return response.json()
