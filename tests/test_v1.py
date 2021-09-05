from random import random
from uuid import uuid4

from httpx import Timeout
from pytest import mark as pytest_mark
from qvapay.v1 import QvaPayAuth, QvaPayClient, QvaPayError

TIMEOUT = 20


def test_error():
    client = QvaPayClient("", "")
    try:
        client.get_info()
        assert False
    except QvaPayError:
        assert True


def test_get_info():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    client.get_info()


def test_get_balance():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    client.get_balance()


def test_create_invoice():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    client.create_invoice(random(), "Invoice for testing", str(uuid4()))


def test_get_transactions():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    result = client.get_transactions()
    if result.data:
        item = result.data[0]
        client.get_transaction(item.id)


@pytest_mark.asyncio
async def test_error_async():
    client = QvaPayClient("", "")
    try:
        await client.get_info_async()
        assert False
    except QvaPayError:
        assert True


@pytest_mark.asyncio
async def test_get_info_async():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    await client.get_info_async()


@pytest_mark.asyncio
async def test_get_balance_async():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    await client.get_balance_async()


@pytest_mark.asyncio
async def test_create_invoice_async():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    await client.create_invoice_async(random(), "Invoice for testing", str(uuid4()))


@pytest_mark.asyncio
async def test_get_transactions_async():
    client = QvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    result = await client.get_transactions_async()
    if result.data:
        item = result.data[0]
        await client.get_transaction_async(item.id)
