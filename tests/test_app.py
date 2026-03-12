from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.app import AppModule as AsyncAppModule
from qvapay._sync.modules.app import AppModule as SyncAppModule
from qvapay.errors import QvaPayError
from qvapay.models.app import App

APP_DATA = {
    "uuid": "abc123",
    "name": "UptimeRobot",
    "url": "https://uptimerobot.com/",
    "logo": "https://media.qvapay.com/apps/test.png",
    "description": "Uptime Status for Robot",
    "callback": "https://uptimerobot.com/dashboard.php",
    "success_url": "",
    "cancel_url": "",
    "active": True,
    "enabled": True,
    "allowed_payment_auth": False,
    "card": False,
    "created_at": "2021-04-04T17:25:55.000Z",
    "updated_at": "2021-04-04T17:25:55.000Z",
}

LIST_RESPONSE = {"result": "OK", "apps": [APP_DATA]}
GET_RESPONSE = {"result": "OK", "app": APP_DATA}
DELETE_RESPONSE = {"result": "OK", "app": APP_DATA}
CREATE_RESPONSE = {
    "result": "OK",
    "app": {
        "uuid": "def456",
        "secret": "secret123abc",
        "name": "Test App",
        "url": "https://testapp.com",
        "desc": "La test App para conectar pagos con QvaPay",
        "logo": "apps/logo123/image.jpeg",
    },
}
NOT_FOUND_RESPONSE = {"result": "App not found"}


def _mock_response(
    json_data: dict,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/app",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


# -- Model tests -------------------------------------------------------------


class TestApp:
    def test_from_json(self):
        app = App.from_json(APP_DATA)
        assert app.uuid == "abc123"
        assert app.name == "UptimeRobot"
        assert app.description == "Uptime Status for Robot"
        assert app.callback == "https://uptimerobot.com/dashboard.php"
        assert app.active is True
        assert app.enabled is True
        assert app.allowed_payment_auth is False
        assert app.card is False
        assert app.created_at == "2021-04-04T17:25:55.000Z"
        assert app.updated_at == "2021-04-04T17:25:55.000Z"

    def test_from_json_desc_alias(self):
        app = App.from_json(CREATE_RESPONSE["app"])
        assert app.description == "La test App para conectar pagos con QvaPay"
        assert app.secret == "secret123abc"

    def test_from_json_optional_defaults(self):
        minimal = {
            "uuid": "abc",
            "name": "Test",
            "logo": "logo.png",
            "url": "https://test.com",
            "description": "A test app",
            "callback": "https://test.com/cb",
        }
        app = App.from_json(minimal)
        assert app.secret is None
        assert app.created_at is None


# -- Async app module tests --------------------------------------------------


class TestAsyncAppModule:
    @pytest.mark.anyio
    async def test_list(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = AsyncAppModule(http)

        apps = await module.list()

        http.get.assert_called_once_with("app")
        assert len(apps) == 1
        assert isinstance(apps[0], App)
        assert apps[0].uuid == "abc123"

    @pytest.mark.anyio
    async def test_get(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(GET_RESPONSE)
        module = AsyncAppModule(http)

        app = await module.get("abc123")

        http.get.assert_called_once_with("app/abc123")
        assert isinstance(app, App)
        assert app.name == "UptimeRobot"

    @pytest.mark.anyio
    async def test_get_not_found(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(NOT_FOUND_RESPONSE, status_code=404)
        module = AsyncAppModule(http)

        with pytest.raises(QvaPayError) as exc_info:
            await module.get("nonexistent")

        assert exc_info.value.status_code == 404
        assert "App not found" in exc_info.value.status_message

    @pytest.mark.anyio
    async def test_delete(self):
        http = AsyncMock()
        http.delete.return_value = _mock_response(DELETE_RESPONSE)
        module = AsyncAppModule(http)

        app = await module.delete("abc123")

        http.delete.assert_called_once_with("app/abc123")
        assert isinstance(app, App)
        assert app.uuid == "abc123"

    @pytest.mark.anyio
    async def test_update(self):
        http = AsyncMock()
        updated = {**GET_RESPONSE["app"], "name": "Updated Name"}
        http.put.return_value = _mock_response({"result": "OK", "app": updated})
        module = AsyncAppModule(http)

        app = await module.update("abc123", name="Updated Name")

        http.put.assert_called_once_with("app/abc123", json={"name": "Updated Name"})
        assert isinstance(app, App)
        assert app.name == "Updated Name"

    @pytest.mark.anyio
    async def test_create(self):
        http = AsyncMock()
        http.post.return_value = _mock_response(CREATE_RESPONSE)
        module = AsyncAppModule(http)

        app = await module.create(
            name="Test App",
            url="https://testapp.com",
            desc="La test App para conectar pagos con QvaPay",
            callback="https://testapp.com/callback",
        )

        http.post.assert_called_once()
        call_kwargs = http.post.call_args
        assert call_kwargs[0][0] == "app/create"
        assert call_kwargs[1]["data"]["name"] == "Test App"
        assert call_kwargs[1]["data"]["desc"] == (
            "La test App para conectar pagos con QvaPay"
        )
        assert call_kwargs[1]["files"] is None
        assert isinstance(app, App)
        assert app.uuid == "def456"
        assert app.secret is not None

    @pytest.mark.anyio
    async def test_create_with_logo(self):
        http = AsyncMock()
        http.post.return_value = _mock_response(CREATE_RESPONSE)
        module = AsyncAppModule(http)

        logo_bytes = b"fake-image-data"
        await module.create(
            name="Test App",
            url="https://testapp.com",
            desc="Test",
            callback="https://testapp.com/cb",
            logo=logo_bytes,
        )

        call_kwargs = http.post.call_args[1]
        assert call_kwargs["files"] == {"logo": logo_bytes}


# -- Sync app module tests ---------------------------------------------------


class TestSyncAppModule:
    def test_list(self):
        http = MagicMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = SyncAppModule(http)

        apps = module.list()

        http.get.assert_called_once_with("app")
        assert len(apps) == 1
        assert isinstance(apps[0], App)
        assert apps[0].uuid == "abc123"

    def test_get(self):
        http = MagicMock()
        http.get.return_value = _mock_response(GET_RESPONSE)
        module = SyncAppModule(http)

        app = module.get("abc123")

        http.get.assert_called_once_with("app/abc123")
        assert isinstance(app, App)
        assert app.name == "UptimeRobot"

    def test_get_not_found(self):
        http = MagicMock()
        http.get.return_value = _mock_response(NOT_FOUND_RESPONSE, status_code=404)
        module = SyncAppModule(http)

        with pytest.raises(QvaPayError) as exc_info:
            module.get("nonexistent")

        assert exc_info.value.status_code == 404
        assert "App not found" in exc_info.value.status_message

    def test_delete(self):
        http = MagicMock()
        http.delete.return_value = _mock_response(DELETE_RESPONSE)
        module = SyncAppModule(http)

        app = module.delete("abc123")

        http.delete.assert_called_once_with("app/abc123")
        assert isinstance(app, App)
        assert app.uuid == "abc123"

    def test_update(self):
        http = MagicMock()
        updated = {**GET_RESPONSE["app"], "name": "Updated Name"}
        http.put.return_value = _mock_response({"result": "OK", "app": updated})
        module = SyncAppModule(http)

        app = module.update("abc123", name="Updated Name")

        http.put.assert_called_once_with("app/abc123", json={"name": "Updated Name"})
        assert isinstance(app, App)
        assert app.name == "Updated Name"

    def test_create(self):
        http = MagicMock()
        http.post.return_value = _mock_response(CREATE_RESPONSE)
        module = SyncAppModule(http)

        app = module.create(
            name="Test App",
            url="https://testapp.com",
            desc="La test App para conectar pagos con QvaPay",
            callback="https://testapp.com/callback",
        )

        http.post.assert_called_once()
        call_kwargs = http.post.call_args
        assert call_kwargs[0][0] == "app/create"
        assert call_kwargs[1]["data"]["name"] == "Test App"
        assert call_kwargs[1]["files"] is None
        assert isinstance(app, App)
        assert app.uuid == "def456"
        assert app.secret is not None
