from random import random
from uuid import uuid4

from httpx import Timeout
from pytest import mark as pytest_mark
from qvapay.v1 import AsyncQvaPayClient, QvaPayAuth, QvaPayError

TIMEOUT = 20


@pytest_mark.anyio
async def test_error():
    client = AsyncQvaPayClient("", "")
    try:
        await client.get_info()
        assert False
    except QvaPayError:
        assert True


@pytest_mark.anyio
async def test_get_info():
    client = AsyncQvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    await client.get_info()


@pytest_mark.anyio
async def test_get_balance():
    client = AsyncQvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    await client.get_balance()


@pytest_mark.anyio
async def test_create_invoice():
    client = AsyncQvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    await client.create_invoice(random(), "Invoice for testing", str(uuid4()))


@pytest_mark.anyio
async def test_get_transactions():
    async with AsyncQvaPayClient.from_auth(
        QvaPayAuth(), timeout=Timeout(TIMEOUT)
    ) as client:
        result = await client.get_transactions()
        if result.data:
            item = result.data[0]
            await client.get_transaction(item.id)
