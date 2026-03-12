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
    async with _client(timeout) as client:
        response = await client.post("auth/register", json=payload)
        validate_response(response)
        return AuthToken.from_json(response.json())


async def request_pin(
    email: str,
    password: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> None:
    """Request a temporary login PIN using email and password."""
    async with _client(timeout) as client:
        response = await client.post(
            "auth/request-pin",
            json={"email": email, "password": password},
        )
        validate_response(response)


async def check(
    access_token: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> None:
    """Check if an access token is valid. Raises QvaPayError if not."""
    headers = {"Authorization": f"Bearer {access_token}"}
    async with _client(timeout, headers=headers) as client:
        response = await client.post("auth/check")
        validate_response(response)


async def logout(
    access_token: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> None:
    """Logout and invalidate the given access token."""
    headers = {"Authorization": f"Bearer {access_token}"}
    async with _client(timeout, headers=headers) as client:
        response = await client.get("auth/logout")
        validate_response(response)
