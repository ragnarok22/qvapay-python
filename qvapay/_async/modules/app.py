from typing import Any, List

from httpx import AsyncClient

from ...models.app import App
from ...utils import validate_response


class AppModule:
    def __init__(self, http: AsyncClient):
        self._http = http

    async def list(self) -> List[App]:
        """Get all apps."""
        response = await self._http.get("app")
        validate_response(response)
        return [App.from_json(item) for item in response.json()["apps"]]

    async def get(self, uuid: str) -> App:
        """Get an app by UUID."""
        response = await self._http.get(f"app/{uuid}")
        validate_response(response)
        return App.from_json(response.json()["app"])

    async def delete(self, uuid: str) -> App:
        """Delete an app by UUID. Returns the deleted app."""
        response = await self._http.delete(f"app/{uuid}")
        validate_response(response)
        return App.from_json(response.json()["app"])

    async def create(self, **kwargs: Any) -> App:
        """Create a new dev app."""
        response = await self._http.post("app", json=kwargs)
        validate_response(response)
        return App.from_json(response.json())
