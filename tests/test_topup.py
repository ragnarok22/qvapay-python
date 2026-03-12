from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.topup import TopupModule as AsyncTopupModule
from qvapay._sync.modules.topup import TopupModule as SyncTopupModule
from qvapay.errors import QvaPayError

PRODUCTS_DATA = [
    {
        "id": 1,
        "name": "Cubacel 250 CUP",
        "price": 2.50,
        "currency": "USD",
    },
    {
        "id": 2,
        "name": "Cubacel 500 CUP",
        "price": 5.00,
        "currency": "USD",
    },
]


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/topup/products",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


# -- Async topup module tests -------------------------------------------------


class TestAsyncTopupModule:
    @pytest.mark.anyio
    async def test_list_products(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(PRODUCTS_DATA)
        module = AsyncTopupModule(http)

        products = await module.list_products()

        http.get.assert_called_once_with("topup/products")
        assert products == PRODUCTS_DATA
        assert len(products) == 2
        assert products[0]["name"] == "Cubacel 250 CUP"

    @pytest.mark.anyio
    async def test_list_products_error(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(
            {"error": "Unauthorized"}, status_code=401
        )
        module = AsyncTopupModule(http)

        with pytest.raises(QvaPayError) as exc_info:
            await module.list_products()

        assert exc_info.value.status_code == 401


# -- Sync topup module tests --------------------------------------------------


class TestSyncTopupModule:
    def test_list_products(self):
        http = MagicMock()
        http.get.return_value = _mock_response(PRODUCTS_DATA)
        module = SyncTopupModule(http)

        products = module.list_products()

        http.get.assert_called_once_with("topup/products")
        assert products == PRODUCTS_DATA
        assert len(products) == 2

    def test_list_products_error(self):
        http = MagicMock()
        http.get.return_value = _mock_response(
            {"error": "Unauthorized"}, status_code=401
        )
        module = SyncTopupModule(http)

        with pytest.raises(QvaPayError):
            module.list_products()
