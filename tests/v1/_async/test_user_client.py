from os import environ

import pytest
from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from qvapay.v1 import AsyncQvaPayUserClient
from qvapay.v1._async.auth_api import login

TIMEOUT = 20


@fixture(name="user_client")
async def create_user_client():
    email = environ.get("QVAPAY_EMAIL", "")
    password = environ.get("QVAPAY_PASSWORD", "")
    if not email or not password:
        pytest.skip("QVAPAY_EMAIL and QVAPAY_PASSWORD not set")
    token = await login(email, password, timeout=Timeout(TIMEOUT))
    client = AsyncQvaPayUserClient(token.access_token, timeout=Timeout(TIMEOUT))
    yield client
    await client.close()


@pytest_mark.anyio
async def test_get_user(user_client: AsyncQvaPayUserClient):
    user = await user_client.get_user()
    assert user.id
    assert user.username


@pytest_mark.anyio
async def test_get_transactions(user_client: AsyncQvaPayUserClient):
    result = await user_client.get_transactions()
    if result.data:
        item = result.data[0]
        await user_client.get_transaction(item.id)


@pytest_mark.anyio
async def test_get_services(user_client: AsyncQvaPayUserClient):
    await user_client.get_services()


@pytest_mark.anyio
async def test_get_payment_links(user_client: AsyncQvaPayUserClient):
    await user_client.get_payment_links()


@pytest_mark.anyio
async def test_get_p2p_offers(user_client: AsyncQvaPayUserClient):
    await user_client.get_p2p_offers()


@pytest_mark.anyio
async def test_get_withdrawals(user_client: AsyncQvaPayUserClient):
    await user_client.get_withdrawals()
