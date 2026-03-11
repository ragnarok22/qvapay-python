from os import environ

from httpx import Timeout

from qvapay.v1 import QvaPayError
from qvapay.v1._sync.auth_api import login, logout

TIMEOUT = 20


def test_login_invalid_credentials():
    try:
        login("invalid@example.com", "wrongpassword", timeout=Timeout(TIMEOUT))
        assert False
    except QvaPayError:
        assert True


def test_login_and_logout():
    email = environ.get("QVAPAY_EMAIL", "")
    password = environ.get("QVAPAY_PASSWORD", "")
    if not email or not password:
        return
    token = login(email, password, timeout=Timeout(TIMEOUT))
    assert token.access_token
    assert token.token_type
    logout(token.access_token, timeout=Timeout(TIMEOUT))
