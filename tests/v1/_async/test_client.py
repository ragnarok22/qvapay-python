from random import random
from uuid import uuid4

from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from qvapay.v1 import AsyncQvaPayClient, QvaPayAuth, QvaPayError

TIMEOUT = 20


@fixture(name="client")
async def create_client():
    client = AsyncQvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    yield client
    await client.close()


@pytest_mark.anyio
async def test_error():
    client = AsyncQvaPayClient("", "")
    try:
        await client.get_info()
        assert False
    except QvaPayError:
        assert True


@pytest_mark.anyio
async def test_get_info(client: AsyncQvaPayClient):
    await client.get_info()


@pytest_mark.anyio
async def test_get_balance(client: AsyncQvaPayClient):
    await client.get_balance()


@pytest_mark.anyio
async def test_create_invoice(client: AsyncQvaPayClient):
    await client.create_invoice(random(), "Invoice for testing", str(uuid4()))


@pytest_mark.anyio
async def test_get_transactions(client: AsyncQvaPayClient):
    result = await client.get_transactions()
    if result.data:
        item = result.data[0]
        await client.get_transaction(item.id)
