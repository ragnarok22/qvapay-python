from typing import List

from httpx import AsyncClient

from ...models.product import Product
from ...utils import validate_response


class StoreModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def products(self) -> List[Product]:
        """Get available products."""
        response = await self._http.get("store/products")
        validate_response(response)
        return [Product.from_json(p) for p in response.json()]

    async def my_purchased(self) -> List[Product]:
        """Get my purchased products."""
        response = await self._http.get("store/my_products")
        validate_response(response)
        return [Product.from_json(p) for p in response.json()]

    async def get_purchased(self, uuid: str) -> Product:
        """Get details of a purchased product."""
        response = await self._http.get(f"store/my_products/{uuid}")
        validate_response(response)
        return Product.from_json(response.json())
