from typing import Any, Optional

from ..http import BASE_URL, DEFAULT_TIMEOUT, AsyncClient, TimeoutTypes
from ..models.auth_token import AuthToken
from ..utils import validate_response


def _client(timeout: TimeoutTypes, **kwargs) -> AsyncClient:
    return AsyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
        **kwargs,
    )


async def login(
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
    async with _client(timeout) as client:
        response = await client.post("auth/login", json=payload)
        validate_response(response)
        return AuthToken.from_json(response.json())


async def register(
    name: str,
    email: str,
    password: str,
    c_password: str,
    invite: str = "",
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> AuthToken:
    """Register a new user account. Returns an AuthToken."""
    payload = {
        "name": name,
        "email": email,
        "password": password,
        "c_password": c_password,
    }
    if invite:
        payload["invite"] = invite
    async with _client(timeout) as client:
        response = await client.post("auth/register", json=payload)
        validate_response(response)
        return AuthToken.from_json(response.json())


async def request_pin(
    email: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> None:
    """Request a PIN code to the given email."""
    async with _client(timeout) as client:
        response = await client.post(
            "auth/request_pin",
            json={"email": email},
        )
        validate_response(response)


async def check(
    access_token: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> dict:
    """Check if an access token is valid."""
    headers = {"Authorization": f"Bearer {access_token}"}
    async with _client(timeout, headers=headers) as client:
        response = await client.post("auth/check")
        validate_response(response)
        return response.json()


async def logout(
    access_token: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> None:
    """Logout and invalidate the given access token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    async with _client(timeout, headers=headers) as client:
        response = await client.get("auth/logout")
        validate_response(response)
