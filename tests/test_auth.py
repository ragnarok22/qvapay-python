from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from qvapay._async import auth as async_auth
from qvapay._sync import auth as sync_auth
from qvapay.errors import QvaPayError
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

REGISTER_RESPONSE = {
    "message": "¡Bienvenido a QvaPay Juan Perez!",
    "accessToken": "17|pnKrh9BbjwgsnHrEumugIcJ3WK19hsD844dzxgbJ",
}

REGISTER_ERROR_RESPONSE = {
    "errors": ["El valor del campo email ya está en uso."],
}

LOGIN_ERROR_PASSWORD = {"error": "Password mismatch"}

LOGIN_ERROR_VALIDATION = {
    "error": [
        "El campo email es obligatorio.",
        "El campo password es obligatorio.",
    ],
}


def _mock_response(
    json_data: dict,
    status_code: int = 200,
    url: str = "https://api.qvapay.com/auth/login",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request("POST", url),
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

    def test_from_json_register_response(self):
        token = AuthToken.from_json(REGISTER_RESPONSE)
        assert token.access_token == "17|pnKrh9BbjwgsnHrEumugIcJ3WK19hsD844dzxgbJ"
        assert token.token_type == "Bearer"
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


# ── Async register tests ─────────────────────────────────────────────


class TestAsyncRegister:
    @pytest.mark.anyio
    async def test_register_basic(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_RESPONSE, status_code=201
        )
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            result = await async_auth.register("Juan", "juan@example.com", "secret123")

        mock_client.post.assert_called_once_with(
            "auth/register",
            json={
                "name": "Juan",
                "email": "juan@example.com",
                "password": "secret123",
                "terms": True,
            },
        )
        assert isinstance(result, AuthToken)
        assert result.access_token == "17|pnKrh9BbjwgsnHrEumugIcJ3WK19hsD844dzxgbJ"
        assert result.me is None

    @pytest.mark.anyio
    async def test_register_with_all_params(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_RESPONSE, status_code=201
        )
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            await async_auth.register(
                "Juan",
                "juan@example.com",
                "secret123",
                lastname="Perez",
                invite="abc",
            )

        payload = mock_client.post.call_args[1]["json"]
        assert payload["lastname"] == "Perez"
        assert payload["invite"] == "abc"

    @pytest.mark.anyio
    async def test_register_excludes_optional_when_not_set(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_RESPONSE, status_code=201
        )
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            await async_auth.register("A", "a@b.com", "pw")

        payload = mock_client.post.call_args[1]["json"]
        assert "lastname" not in payload
        assert "invite" not in payload

    @pytest.mark.anyio
    async def test_register_422_raises_error(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_ERROR_RESPONSE, status_code=422
        )
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            with pytest.raises(QvaPayError) as exc_info:
                await async_auth.register("A", "dup@b.com", "pw")

        assert exc_info.value.status_code == 422
        assert "email" in exc_info.value.status_message


# ── Sync register tests ──────────────────────────────────────────────


class TestSyncRegister:
    def test_register_basic(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_RESPONSE, status_code=201
        )
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            result = sync_auth.register("Juan", "juan@example.com", "secret123")

        mock_client.post.assert_called_once_with(
            "auth/register",
            json={
                "name": "Juan",
                "email": "juan@example.com",
                "password": "secret123",
                "terms": True,
            },
        )
        assert isinstance(result, AuthToken)
        assert result.access_token == "17|pnKrh9BbjwgsnHrEumugIcJ3WK19hsD844dzxgbJ"

    def test_register_with_all_params(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_RESPONSE, status_code=201
        )
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            sync_auth.register(
                "Juan",
                "juan@example.com",
                "secret123",
                lastname="Perez",
                invite="abc",
            )

        payload = mock_client.post.call_args[1]["json"]
        assert payload["lastname"] == "Perez"
        assert payload["invite"] == "abc"

    def test_register_422_raises_error(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_ERROR_RESPONSE, status_code=422
        )
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            with pytest.raises(QvaPayError) as exc_info:
                sync_auth.register("A", "dup@b.com", "pw")

        assert exc_info.value.status_code == 422
        assert "email" in exc_info.value.status_message


# ── Async request_pin tests ──────────────────────────────────────────


class TestAsyncRequestPin:
    @pytest.mark.anyio
    async def test_request_pin(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response({}, status_code=200)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            result = await async_auth.request_pin("user@example.com")

        mock_client.post.assert_called_once_with(
            "auth/request_pin",
            json={"email": "user@example.com"},
        )
        assert result is None

    @pytest.mark.anyio
    async def test_request_pin_422_raises_error(self):
        mock_client = AsyncMock()
        mock_client.post.return_value = _mock_response(
            LOGIN_ERROR_VALIDATION, status_code=422
        )
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.auth._client", return_value=mock_client):
            with pytest.raises(QvaPayError) as exc_info:
                await async_auth.request_pin("")

        assert exc_info.value.status_code == 422
        assert "email" in exc_info.value.status_message


# ── Sync request_pin tests ───────────────────────────────────────────


class TestSyncRequestPin:
    def test_request_pin(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response({}, status_code=200)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            result = sync_auth.request_pin("user@example.com")

        mock_client.post.assert_called_once_with(
            "auth/request_pin",
            json={"email": "user@example.com"},
        )
        assert result is None

    def test_request_pin_422_raises_error(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(
            LOGIN_ERROR_VALIDATION, status_code=422
        )
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            with pytest.raises(QvaPayError) as exc_info:
                sync_auth.request_pin("")

        assert exc_info.value.status_code == 422
        assert "email" in exc_info.value.status_message


# ── Error handling tests ─────────────────────────────────────────────


class TestErrorHandling:
    def test_login_password_mismatch(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(
            LOGIN_ERROR_PASSWORD, status_code=422
        )
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            with pytest.raises(QvaPayError) as exc_info:
                sync_auth.login("user@example.com", "wrong")

        assert exc_info.value.status_code == 422
        assert exc_info.value.status_message == "Password mismatch"

    def test_login_validation_errors_as_list(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(
            LOGIN_ERROR_VALIDATION, status_code=422
        )
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            with pytest.raises(QvaPayError) as exc_info:
                sync_auth.login("", "")

        assert exc_info.value.status_code == 422
        assert "email" in exc_info.value.status_message
        assert "password" in exc_info.value.status_message

    def test_register_errors_list(self):
        mock_client = MagicMock()
        mock_client.post.return_value = _mock_response(
            REGISTER_ERROR_RESPONSE, status_code=422
        )
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.auth._client", return_value=mock_client):
            with pytest.raises(QvaPayError) as exc_info:
                sync_auth.register("A", "dup@b.com", "pw")

        assert exc_info.value.status_code == 422
        assert "email" in exc_info.value.status_message
