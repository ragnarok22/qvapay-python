from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from qvapay._async import stocks as async_stocks
from qvapay._sync import stocks as sync_stocks

LIST_RESPONSE = [
    {"symbol": "AAPL", "price": 213.07},
    {"symbol": "MSFT", "price": 378.91},
    {"symbol": "TSLA", "price": 174.12},
]


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/stocks/index",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


# -- Async module tests ------------------------------------------------------


class TestAsyncStocksList:
    @pytest.mark.anyio
    async def test_list(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(LIST_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.stocks._client", return_value=mock_client):
            result = await async_stocks.list()

        mock_client.get.assert_called_once_with("stocks/index")
        assert len(result) == 3
        assert result[0]["symbol"] == "AAPL"
        assert result[1]["price"] == 378.91
        assert result[2]["symbol"] == "TSLA"


# -- Sync module tests -------------------------------------------------------


class TestSyncStocksList:
    def test_list(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.stocks._client", return_value=mock_client):
            result = sync_stocks.list()

        mock_client.get.assert_called_once_with("stocks/index")
        assert len(result) == 3
        assert result[0]["symbol"] == "AAPL"
        assert result[1]["price"] == 378.91
        assert result[2]["symbol"] == "TSLA"
