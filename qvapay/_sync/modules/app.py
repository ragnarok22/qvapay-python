from typing import Any, List

from httpx import Client

from ...models.app import App
from ...utils import validate_response


class AppModule:
    def __init__(self, http: Client):
        self._http = http

    def list(self) -> List[App]:
        """Get all apps."""
        response = self._http.get("app")
        validate_response(response)
        return [App.from_json(item) for item in response.json()]

    def get(self, uuid: str) -> App:
        """Get an app by UUID."""
        response = self._http.get(f"app/{uuid}")
        validate_response(response)
        return App.from_json(response.json())

    def delete(self, uuid: str) -> None:
        """Delete an app by UUID."""
        response = self._http.delete(f"app/{uuid}")
        validate_response(response)

    def create(self, **kwargs: Any) -> App:
        """Create a new dev app."""
        response = self._http.post("app", json=kwargs)
        validate_response(response)
        return App.from_json(response.json())
