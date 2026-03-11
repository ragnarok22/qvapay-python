from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from qvapay._async import auth as async_auth
from qvapay._sync import auth as sync_auth
from qvapay.models.auth_token import AuthToken
from qvapay.models.user import User

LOGIN_RESPONSE = {
    "accessToken": "104510|$2b$10$QzRetQodABPVePrtMx95P",
    "token_type": "Bearer",
    "me": {
        "uuid": "12b1e145-82ce-480a-b5c6-1a681a125f0a",
        "username": "skymind",
        "name": "SkyMind",
        "lastname": "Payments",
        "email": "ceo@skymind.ltd",
        "bio": "Soluciones Fintech a la medida.",
        "address": "",
        "image": "profiles/avatar.png",
        "cover": "covers/banner.jpg",
        "balance": "90.59",
        "pending_balance": "0",
        "satoshis": 2424,
        "createdAt": "2024-01-28T23:24:54.000Z",
        "updatedAt": "2025-07-19T16:49:01.000Z",
        "phone": "+17867918868",
        "phone_verified": True,
        "telegram": "",
        "twitter": None,
        "kyc": True,
        "vip": True,
        "golden_check": False,
        "pin": 1111,
        "last_seen": "2025-07-19T16:49:01.000Z",
        "telegram_id": "7427512552",
        "role": "admin",
        "p2p_enabled": True,
    },
}


def _mock_response(json_data: dict) -> httpx.Response:
    return httpx.Response(
        status_code=200,
        json=json_data,
        request=httpx.Request("POST", "https://api.qvapay.com/auth/login"),
    )


# ── Model tests ──────────────────────────────────────────────────────


class TestUser:
    def test_from_json(self):
        user = User.from_json(LOGIN_RESPONSE["me"])
        assert user.uuid == "12b1e145-82ce-480a-b5c6-1a681a125f0a"
        assert user.username == "skymind"
        assert user.name == "SkyMind"
        assert user.lastname == "Payments"
        assert user.email == "ceo@skymind.ltd"
        assert user.balance == "90.59"
        assert user.satoshis == 2424
        assert user.kyc is True
        assert user.vip is True
        assert user.golden_check is False
        assert user.pin == 1111
        assert user.role == "admin"
        assert user.p2p_enabled is True

    def test_from_json_camel_case_aliases(self):
        user = User.from_json(LOGIN_RESPONSE["me"])
        assert user.created_at == "2024-01-28T23:24:54.000Z"
        assert user.updated_at == "2025-07-19T16:49:01.000Z"

    def test_from_json_optional_fields_default_none(self):
        user = User.from_json(
            {
                "uuid": "abc",
                "username": "test",
                "name": "Test",
                "lastname": "User",
                "email": "test@test.com",
            }
        )
        assert user.balance is None
        assert user.phone is None
        assert user.created_at is None


class TestAuthToken:
    def test_from_json_aliases_access_token(self):
        token = AuthToken.from_json(LOGIN_RESPONSE)
        assert token.access_token == "104510|$2b$10$QzRetQodABPVePrtMx95P"
        assert token.token_type == "Bearer"

    def test_from_json_deserializes_me(self):
        token = AuthToken.from_json(LOGIN_RESPONSE)
        assert isinstance(token.me, User)
        assert token.me.uuid == "12b1e145-82ce-480a-b5c6-1a681a125f0a"
        assert token.me.username == "skymind"

    def test_from_json_without_me(self):
        data = {"accessToken": "tok123", "token_type": "Bearer"}
        token = AuthToken.from_json(data)
        assert token.access_token == "tok123"
        assert token.me is None


# ── Async login tests ────────────────────────────────────────────────


class TestAsyncLogin:
    @pytest.mark.anyio
    async def test_login_basic(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(LOGIN_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            result = await async_auth.login("user@example.com", "secret")

        mock_client.post.assert_called_once_with(
            "auth/login",
            json={"email": "user@example.com", "password": "secret"},
        )
        assert isinstance(result, AuthToken)
        assert result.access_token == "104510|$2b$10$QzRetQodABPVePrtMx95P"
        assert isinstance(result.me, User)

    @pytest.mark.anyio
    async def test_login_with_two_factor(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(LOGIN_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            result = await async_auth.login(
                "user@example.com",
                "secret",
                two_factor_code="1234",
                remember=True,
            )

        mock_client.post.assert_called_once_with(
            "auth/login",
            json={
                "email": "user@example.com",
                "password": "secret",
                "two_factor_code": "1234",
                "remember": True,
            },
        )
        assert isinstance(result, AuthToken)

    @pytest.mark.anyio
    async def test_login_without_optional_params_excludes_them(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(LOGIN_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            await async_auth.login("a@b.com", "pw")

        payload = mock_client.post.call_args[1]["json"]
        assert "two_factor_code" not in payload
        assert "remember" not in payload


# ── Sync login tests ─────────────────────────────────────────────────


class TestSyncLogin:
    def test_login_basic(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(LOGIN_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            result = sync_auth.login("user@example.com", "secret")

        mock_client.post.assert_called_once_with(
            "auth/login",
            json={"email": "user@example.com", "password": "secret"},
        )
        assert isinstance(result, AuthToken)
        assert result.access_token == "104510|$2b$10$QzRetQodABPVePrtMx95P"
        assert isinstance(result.me, User)

    def test_login_with_two_factor(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(LOGIN_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            result = sync_auth.login(
                "user@example.com",
                "secret",
                two_factor_code="1234",
                remember=True,
            )

        mock_client.post.assert_called_once_with(
            "auth/login",
            json={
                "email": "user@example.com",
                "password": "secret",
                "two_factor_code": "1234",
                "remember": True,
            },
        )
        assert isinstance(result, AuthToken)

    def test_login_without_optional_params_excludes_them(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(LOGIN_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            sync_auth.login("a@b.com", "pw")

        payload = mock_client.post.call_args[1]["json"]
        assert "two_factor_code" not in payload
        assert "remember" not in payload
