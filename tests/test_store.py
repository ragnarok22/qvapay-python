from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.store import StoreModule as AsyncStoreModule
from qvapay._sync.modules.store import StoreModule as SyncStoreModule
from qvapay.models.product import Product
from qvapay.models.purchased_product import PurchasedProduct

PRODUCT_PAYLOAD = {
    "uuid": "e286449c-5bf4-4fbc-9a85-95bb5b54c73e",
    "name": "Saldo movil ETECSA",
    "lead": "$ 250 CUP",
    "price": "7.50",
    "logo": "services/etecsa.png",
    "sublogo": "services/etecsa-cover.png",
    "desc": "Compre paquetes de saldo movil ETECSA.",
}

PURCHASED_PAYLOAD = {
    "id": 6003,
    "service_id": 2,
    "service_data": '{"name":"Pedro"}',
    "notes": "",
    "status": "pending",
    "amount": "5.00",
    "transaction_id": 767745,
    "notified": "no",
    "created_at": "2023-07-18T04:07:58.000000Z",
    "updated_at": "2023-07-18T04:07:58.000000Z",
}


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/store",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


class TestAsyncStoreModule:
    @pytest.mark.anyio
    async def test_products_unwraps_paginated_data(self):
        http = AsyncMock()
        http.get.return_value = _mock_response({"data": [PRODUCT_PAYLOAD]})
        module = AsyncStoreModule(http)

        products = await module.products()

        http.get.assert_called_once_with("store")
        assert len(products) == 1
        assert isinstance(products[0], Product)
        assert products[0].description == "Compre paquetes de saldo movil ETECSA."

    @pytest.mark.anyio
    async def test_my_purchased_returns_purchase_records(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(
            {"data": [PURCHASED_PAYLOAD]},
            url="https://api.qvapay.com/store/my",
        )
        module = AsyncStoreModule(http)

        purchases = await module.my_purchased()

        http.get.assert_called_once_with("store/my")
        assert len(purchases) == 1
        assert isinstance(purchases[0], PurchasedProduct)
        assert purchases[0].amount == 5.0
        assert purchases[0].transaction_id == 767745


class TestSyncStoreModule:
    def test_products_unwraps_paginated_data(self):
        http = MagicMock()
        http.get.return_value = _mock_response({"data": [PRODUCT_PAYLOAD]})
        module = SyncStoreModule(http)

        products = module.products()

        http.get.assert_called_once_with("store")
        assert len(products) == 1
        assert isinstance(products[0], Product)
        assert products[0].description == "Compre paquetes de saldo movil ETECSA."

    def test_my_purchased_returns_purchase_records(self):
        http = MagicMock()
        http.get.return_value = _mock_response(
            {"data": [PURCHASED_PAYLOAD]},
            url="https://api.qvapay.com/store/my",
        )
        module = SyncStoreModule(http)

        purchases = module.my_purchased()

        http.get.assert_called_once_with("store/my")
        assert len(purchases) == 1
        assert isinstance(purchases[0], PurchasedProduct)
        assert purchases[0].amount == 5.0
        assert purchases[0].transaction_id == 767745
