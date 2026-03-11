from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.payment_links import (
    PaymentLinksModule as AsyncPaymentLinksModule,
)
from qvapay._sync.modules.payment_links import (
    PaymentLinksModule as SyncPaymentLinksModule,
)
from qvapay.models.payment_link import PaymentLink

LINK_DATA = {
    "name": "Pulover de guinga azul",
    "product_id": "PVG-AZUL",
    "amount": "10.32",
    "created_at": "2022-04-19T21:42:04.000000Z",
    "updated_at": "2022-04-19T21:42:04.000000Z",
    "payment_link_url": "https://qvapay3.test/payme/wpiuwe/10.32",
}

LINK_DATA_2 = {
    "name": "Camiseta blanca",
    "product_id": "CAM-BLA",
    "amount": "25.00",
    "created_at": "2022-04-20T10:00:00.000000Z",
    "updated_at": "2022-04-20T10:00:00.000000Z",
    "payment_link_url": "https://qvapay3.test/payme/xyz/25.00",
}

LIST_RESPONSE = [LINK_DATA, LINK_DATA_2]

CREATE_RESPONSE = {
    "name": "Nuevo producto",
    "product_id": "NP-001",
    "amount": "50.00",
    "created_at": "2022-05-01T12:00:00.000000Z",
    "updated_at": "2022-05-01T12:00:00.000000Z",
    "payment_link_url": "https://qvapay3.test/payme/abc/50.00",
}


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/payment_links",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


# -- Model tests -------------------------------------------------------------


class TestPaymentLink:
    def test_from_json(self):
        link = PaymentLink.from_json(LINK_DATA)
        assert link.name == "Pulover de guinga azul"
        assert link.product_id == "PVG-AZUL"
        assert link.amount == "10.32"
        assert link.payment_link_url == "https://qvapay3.test/payme/wpiuwe/10.32"
        assert link.created_at == "2022-04-19T21:42:04.000000Z"
        assert link.updated_at == "2022-04-19T21:42:04.000000Z"

    def test_from_json_minimal(self):
        minimal = {
            "name": "Test",
            "product_id": "T-1",
            "amount": "1.00",
        }
        link = PaymentLink.from_json(minimal)
        assert link.name == "Test"
        assert link.product_id == "T-1"
        assert link.amount == "1.00"
        assert link.payment_link_url is None
        assert link.created_at is None
        assert link.updated_at is None


# -- Async module tests ------------------------------------------------------


class TestAsyncPaymentLinksModule:
    @pytest.mark.anyio
    async def test_list(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = AsyncPaymentLinksModule(http)

        links = await module.list()

        http.get.assert_called_once_with("payment_links")
        assert len(links) == 2
        assert isinstance(links[0], PaymentLink)
        assert links[0].name == "Pulover de guinga azul"
        assert links[0].product_id == "PVG-AZUL"
        assert links[1].name == "Camiseta blanca"

    @pytest.mark.anyio
    async def test_create(self):
        http = AsyncMock()
        http.post.return_value = _mock_response(CREATE_RESPONSE)
        module = AsyncPaymentLinksModule(http)

        link = await module.create(
            name="Nuevo producto",
            product_id="NP-001",
            amount="50.00",
        )

        http.post.assert_called_once_with(
            "payment_links",
            json={
                "name": "Nuevo producto",
                "product_id": "NP-001",
                "amount": "50.00",
            },
        )
        assert isinstance(link, PaymentLink)
        assert link.name == "Nuevo producto"
        assert link.amount == "50.00"
        assert link.payment_link_url == "https://qvapay3.test/payme/abc/50.00"


# -- Sync module tests -------------------------------------------------------


class TestSyncPaymentLinksModule:
    def test_list(self):
        http = MagicMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = SyncPaymentLinksModule(http)

        links = module.list()

        http.get.assert_called_once_with("payment_links")
        assert len(links) == 2
        assert isinstance(links[0], PaymentLink)
        assert links[0].name == "Pulover de guinga azul"
        assert links[0].product_id == "PVG-AZUL"
        assert links[1].name == "Camiseta blanca"

    def test_create(self):
        http = MagicMock()
        http.post.return_value = _mock_response(CREATE_RESPONSE)
        module = SyncPaymentLinksModule(http)

        link = module.create(
            name="Nuevo producto",
            product_id="NP-001",
            amount="50.00",
        )

        http.post.assert_called_once_with(
            "payment_links",
            json={
                "name": "Nuevo producto",
                "product_id": "NP-001",
                "amount": "50.00",
            },
        )
        assert isinstance(link, PaymentLink)
        assert link.name == "Nuevo producto"
        assert link.amount == "50.00"
        assert link.payment_link_url == "https://qvapay3.test/payme/abc/50.00"
