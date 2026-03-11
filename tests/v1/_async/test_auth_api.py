from os import environ

import pytest
from httpx import Timeout
from pytest import mark as pytest_mark

from qvapay.v1 import QvaPayError
from qvapay.v1._async.auth_api import login, logout

TIMEOUT = 20


@pytest_mark.anyio
async def test_login_invalid_credentials():
    with pytest.raises(QvaPayError):
        await login("invalid@example.com", "wrongpassword", timeout=Timeout(TIMEOUT))


@pytest_mark.anyio
async def test_login_and_logout():
    email = environ.get("QVAPAY_EMAIL", "")
    password = environ.get("QVAPAY_PASSWORD", "")
    if not email or not password:
        pytest.skip("QVAPAY_EMAIL and QVAPAY_PASSWORD not set")
    token = await login(email, password, timeout=Timeout(TIMEOUT))
    assert token.access_token
    assert token.token_type
    await logout(token.access_token, timeout=Timeout(TIMEOUT))
