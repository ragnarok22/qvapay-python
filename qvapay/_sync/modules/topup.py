from typing import Any, List

from httpx import Client

from ...utils import validate_response


class TopupModule:
    def __init__(self, http: Client):
        self._http = http

    def list_products(self) -> List[Any]:
        """List available phone top-up products."""
        response = self._http.get("topup/products")
        validate_response(response)
        return response.json()
