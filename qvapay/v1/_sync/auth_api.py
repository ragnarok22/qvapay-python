from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..http_clients import SyncClient
from ..models.auth_token import AuthToken
from ..utils import validate_response

BASE_URL = "https://qvapay.com/api"


def login(
    email: str,
    password: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> AuthToken:
    """
    Login with email and password.
    Returns an AuthToken with the access_token for authenticated requests.
    """
    with SyncClient(base_url=BASE_URL, timeout=timeout) as client:
        response = client.post(
            "auth/login",
            json={"email": email, "password": password},
        )
        validate_response(response)
        return AuthToken.from_json(response.json())


def register(
    name: str,
    email: str,
    password: str,
    c_password: str,
    invite: str = "",
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> AuthToken:
    """
    Register a new user account.
    Returns an AuthToken with the access_token for authenticated requests.
    """
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "c_password": c_password,
    }
    if invite:
        payload["invite"] = invite
    with SyncClient(base_url=BASE_URL, timeout=timeout) as client:
        response = client.post("auth/register", json=payload)
        validate_response(response)
        return AuthToken.from_json(response.json())


def logout(
    access_token: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> None:
    """Logout and invalidate the given access token."""
    with SyncClient(
        base_url=BASE_URL,
        headers={"Authorization": f"Bearer {access_token}"},
        timeout=timeout,
    ) as client:
        response = client.get("auth/logout")
        validate_response(response)
