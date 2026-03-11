from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.merchant import AsyncQvaPayMerchant
from qvapay._sync.merchant import SyncQvaPayMerchant
from qvapay.models.app import App

APP_UUID = "9955dd29-082f-470b-882d-f4f0f25ea144"
APP_SECRET = "Zx03ncGDTlBFvZ0JRAq61NUkB82pekNKs1PFkBYAAiadfbzg5l"

INFO_RESPONSE = {
    "user_id": 1,
    "name": "TestAPP",
    "url": "https://www.TestAPP.com",
    "desc": "TestAPP",
    "callback": "https://TestAPP.com/api/qvapay/confirmed",
    "success_url": "https://TestAPP.com/confirmed",
    "cancel_url": "https://TestAPP.com/cancelled",
    "logo": "apps/L0YTTe3YdYz9XUh2B78OPdMPNVpt4aVci8FV5y3B.png",
    "uuid": APP_UUID,
    "active": 1,
    "enabled": 1,
    "card": 1,
    "created_at": "2021-01-12T01:34:21.000000Z",
    "updated_at": "2021-01-12T01:34:21.000000Z",
    "app_photo_url": (
        "https://qvapaystatic.nyc3.digitaloceanspaces.com/"
        "apps/L0YTTe3YdYz9XUh2B78OPdMPNVpt4aVci8FV5y3B.png"
    ),
}

AUTH_PAYLOAD = {"app_id": APP_UUID, "app_secret": APP_SECRET}


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "POST",
    url: str = "https://api.qvapay.com/info",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


# -- Auth payload tests ------------------------------------------------------


class TestMerchantAuthPayload:
    @pytest.mark.anyio
    async def test_async_auth_keys(self):
        merchant = AsyncQvaPayMerchant(uuid=APP_UUID, secret_key=APP_SECRET)
        assert merchant._auth == AUTH_PAYLOAD
        await merchant.close()

    def test_sync_auth_keys(self):
        merchant = SyncQvaPayMerchant(uuid=APP_UUID, secret_key=APP_SECRET)
        assert merchant._auth == AUTH_PAYLOAD
        merchant.close()


# -- Async info tests --------------------------------------------------------


class TestAsyncMerchantInfo:
    @pytest.mark.anyio
    async def test_info(self):
        merchant = AsyncQvaPayMerchant(uuid=APP_UUID, secret_key=APP_SECRET)
        merchant._http = AsyncMock()
        merchant._http.post.return_value = _mock_response(INFO_RESPONSE)

        app = await merchant.info()

        merchant._http.post.assert_called_once_with("info", json=AUTH_PAYLOAD)
        assert isinstance(app, App)
        assert app.uuid == APP_UUID
        assert app.name == "TestAPP"
        assert app.description == "TestAPP"
        assert app.url == "https://www.TestAPP.com"
        assert app.callback == "https://TestAPP.com/api/qvapay/confirmed"
        assert app.success_url == "https://TestAPP.com/confirmed"
        assert app.cancel_url == "https://TestAPP.com/cancelled"
        assert app.active is True
        assert app.enabled is True
        assert app.card is True
        assert app.created_at == "2021-01-12T01:34:21.000000Z"

    @pytest.mark.anyio
    async def test_info_extra_fields(self):
        """Extra API fields (user_id, app_photo_url) are stored via setattr."""
        merchant = AsyncQvaPayMerchant(uuid=APP_UUID, secret_key=APP_SECRET)
        merchant._http = AsyncMock()
        merchant._http.post.return_value = _mock_response(INFO_RESPONSE)

        app = await merchant.info()

        assert app.user_id == 1
        assert "qvapaystatic" in app.app_photo_url


# -- Sync info tests ---------------------------------------------------------


class TestSyncMerchantInfo:
    def test_info(self):
        merchant = SyncQvaPayMerchant(uuid=APP_UUID, secret_key=APP_SECRET)
        merchant._http = MagicMock()
        merchant._http.post.return_value = _mock_response(INFO_RESPONSE)

        app = merchant.info()

        merchant._http.post.assert_called_once_with("info", json=AUTH_PAYLOAD)
        assert isinstance(app, App)
        assert app.uuid == APP_UUID
        assert app.name == "TestAPP"
        assert app.description == "TestAPP"
        assert app.active is True
        assert app.enabled is True
