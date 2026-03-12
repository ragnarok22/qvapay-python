from typing import Any, List

from httpx import Client

from ...utils import validate_response


class TopupModule:
    def __init__(self, http: Client):
        self._http = http

    def list_products(self) -> List[Any]:
        """List available phone top-up packages."""
        response = self._http.get("store/phone_package")
        validate_response(response)
        payload = response.json()
        if isinstance(payload, dict) and isinstance(
            payload.get("phone_packages"), list
        ):
            return payload["phone_packages"]
        return payload
