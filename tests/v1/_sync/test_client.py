from random import random
from uuid import uuid4

from httpx import Timeout
from pytest import fixture
from pytest import mark as pytest_mark

from qvapay.v1 import QvaPayAuth, QvaPayError, SyncQvaPayClient

TIMEOUT = 20


@fixture(name="client")
def create_client():
    client = SyncQvaPayClient.from_auth(QvaPayAuth(), timeout=Timeout(TIMEOUT))
    yield client
    client.close()


@pytest_mark.anyio
def test_error():
    client = SyncQvaPayClient("", "")
    try:
        client.get_info()
        assert False
    except QvaPayError:
        assert True


@pytest_mark.anyio
def test_get_info(client: SyncQvaPayClient):
    client.get_info()


@pytest_mark.anyio
def test_get_balance(client: SyncQvaPayClient):
    client.get_balance()


@pytest_mark.anyio
def test_create_invoice(client: SyncQvaPayClient):
    client.create_invoice(random(), "Invoice for testing", str(uuid4()))


@pytest_mark.anyio
def test_get_transactions(client: SyncQvaPayClient):
    result = client.get_transactions()
    if result.data:
        item = result.data[0]
        client.get_transaction(item.id)
