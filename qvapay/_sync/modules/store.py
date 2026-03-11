from typing import Any, List

from httpx import Client

from ...models.product import Product
from ...utils import validate_response


class StoreModule:
    def __init__(self, http: Client):
        self._http = http

    def products(self) -> List[Product]:
        """Get available products."""
        response = self._http.get("store/products")
        validate_response(response)
        return [Product.from_json(p) for p in response.json()]

    def my_purchased(self) -> List[Product]:
        """Get my purchased products."""
        response = self._http.get("store/my_products")
        validate_response(response)
        return [Product.from_json(p) for p in response.json()]

    def get_purchased(self, uuid: str) -> Product:
        """Get details of a purchased product."""
        response = self._http.get(f"store/my_products/{uuid}")
        validate_response(response)
        return Product.from_json(response.json())
