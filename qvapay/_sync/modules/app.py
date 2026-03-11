from typing import BinaryIO, List, Optional, Union

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
        return [App.from_json(item) for item in response.json()["apps"]]

    def get(self, uuid: str) -> App:
        """Get an app by UUID."""
        response = self._http.get(f"app/{uuid}")
        validate_response(response)
        return App.from_json(response.json()["app"])

    def delete(self, uuid: str) -> App:
        """Delete an app by UUID. Returns the deleted app."""
        response = self._http.delete(f"app/{uuid}")
        validate_response(response)
        return App.from_json(response.json()["app"])

    def create(
        self,
        name: str,
        url: str,
        desc: str,
        callback: str,
        logo: Optional[Union[BinaryIO, bytes]] = None,
        success_url: str = "",
        cancel_url: str = "",
    ) -> App:
        """Create a new dev app."""
        data = {
            "name": name,
            "url": url,
            "desc": desc,
            "callback": callback,
            "success_url": success_url,
            "cancel_url": cancel_url,
        }
        files = None
        if logo is not None:
            files = {"logo": logo}
        response = self._http.post("app/create", data=data, files=files)
        validate_response(response)
        return App.from_json(response.json()["app"])
