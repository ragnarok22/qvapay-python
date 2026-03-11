from typing import Any, Optional

from ..http import BASE_URL, DEFAULT_TIMEOUT, SyncClient, TimeoutTypes
from ..models.auth_token import AuthToken
from ..utils import validate_response


def _client(timeout: TimeoutTypes, **kwargs) -> SyncClient:
    return SyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
        **kwargs,
    )


def login(
    email: str,
    password: str,
    two_factor_code: Optional[str] = None,
    remember: bool = False,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> AuthToken:
    """Login with email and password. Returns an AuthToken."""
    payload: dict[str, Any] = {"email": email, "password": password}
    if two_factor_code is not None:
        payload["two_factor_code"] = two_factor_code
    if remember:
        payload["remember"] = True
    with _client(timeout) as client:
        response = client.post("auth/login", json=payload)
        validate_response(response)
        return AuthToken.from_json(response.json())


def register(
    name: str,
    email: str,
    password: str,
    lastname: Optional[str] = None,
    invite: str = "",
    terms: bool = True,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> AuthToken:
    """Register a new user account. Returns an AuthToken."""
    payload: dict[str, Any] = {
        "name": name,
        "email": email,
        "password": password,
        "terms": terms,
    }
    if lastname is not None:
        payload["lastname"] = lastname
    if invite:
        payload["invite"] = invite
    with _client(timeout) as client:
        response = client.post("auth/register", json=payload)
        validate_response(response)
        return AuthToken.from_json(response.json())


def request_pin(
    email: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> None:
    """Request a PIN code to the given email."""
    with _client(timeout) as client:
        response = client.post(
            "auth/request_pin",
            json={"email": email},
        )
        validate_response(response)


def check(
    access_token: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> dict:
    """Check if an access token is valid."""
    headers = {"Authorization": f"Bearer {access_token}"}
    with _client(timeout, headers=headers) as client:
        response = client.post("auth/check")
        validate_response(response)
        return response.json()


def logout(
    access_token: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> None:
    """Logout and invalidate the given access token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    with _client(timeout, headers=headers) as client:
        response = client.get("auth/logout")
        validate_response(response)
