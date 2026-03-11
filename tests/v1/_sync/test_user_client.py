from os import environ

import pytest
from httpx import Timeout
from pytest import fixture

from qvapay.v1 import SyncQvaPayUserClient
from qvapay.v1._sync.auth_api import login

TIMEOUT = 20


@fixture(name="user_client")
def create_user_client():
    email = environ.get("QVAPAY_EMAIL", "")
    password = environ.get("QVAPAY_PASSWORD", "")
    if not email or not password:
        pytest.skip("QVAPAY_EMAIL and QVAPAY_PASSWORD not set")
    token = login(email, password, timeout=Timeout(TIMEOUT))
    client = SyncQvaPayUserClient(token.access_token, timeout=Timeout(TIMEOUT))
    yield client
    client.close()


def test_get_user(user_client: SyncQvaPayUserClient):
    user = user_client.get_user()
    assert user.id
    assert user.username


def test_get_transactions(user_client: SyncQvaPayUserClient):
    result = user_client.get_transactions()
    if result.data:
        item = result.data[0]
        user_client.get_transaction(item.id)


def test_get_services(user_client: SyncQvaPayUserClient):
    user_client.get_services()


def test_get_payment_links(user_client: SyncQvaPayUserClient):
    user_client.get_payment_links()


def test_get_p2p_offers(user_client: SyncQvaPayUserClient):
    user_client.get_p2p_offers()


def test_get_withdrawals(user_client: SyncQvaPayUserClient):
    user_client.get_withdrawals()
