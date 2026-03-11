from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from qvapay._async import stocks as async_stocks
from qvapay._sync import stocks as sync_stocks
from qvapay.models.coin import Coin, CoinCategory

COIN_BTC = {
    "id": 1,
    "coins_categories_id": 1,
    "name": "BitCoin",
    "logo": "btc",
    "tick": "BTC",
    "fee_in": "0.00",
    "fee_out": "7.50",
    "min_in": "30.00",
    "min_out": "20.00",
    "working_data": '[{"name": "Wallet", "type": "text"}]',
    "enabled_in": 1,
    "enabled_out": 1,
    "enabled_p2p": 1,
    "price": "21698.968770779000000000",
    "created_at": None,
    "updated_at": "2022-07-08T17:10:01.000000Z",
}

COIN_ZELLE = {
    "id": 14,
    "coins_categories_id": 2,
    "name": "Zelle",
    "logo": "zelle",
    "tick": "ZELLE",
    "fee_in": "4.00",
    "fee_out": "4.00",
    "min_in": "10.00",
    "min_out": "20.00",
    "working_data": '[{"name": "Nombre y Apellidos", "type": "text"}]',
    "enabled_in": 1,
    "enabled_out": 1,
    "enabled_p2p": 1,
    "price": "1.000000000000000000",
    "created_at": None,
    "updated_at": None,
}

LIST_RESPONSE = [
    {
        "id": 1,
        "name": "Criptomonedas",
        "logo": "crypto",
        "coins": [COIN_BTC],
    },
    {
        "id": 2,
        "name": "Bank",
        "logo": "bank",
        "coins": [COIN_ZELLE],
    },
    {
        "id": 3,
        "name": "Cash",
        "logo": "cash",
        "coins": [],
    },
]


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/coins",
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

        mock_client.get.assert_called_once_with("coins")
        assert len(result) == 3
        assert isinstance(result[0], CoinCategory)
        assert result[0].name == "Criptomonedas"
        assert len(result[0].coins) == 1
        assert isinstance(result[0].coins[0], Coin)
        assert result[0].coins[0].tick == "BTC"
        assert result[1].name == "Bank"
        assert result[1].coins[0].tick == "ZELLE"
        assert result[2].name == "Cash"
        assert result[2].coins == []


# -- Sync module tests -------------------------------------------------------


class TestSyncStocksList:
    def test_list(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.stocks._client", return_value=mock_client):
            result = sync_stocks.list()

        mock_client.get.assert_called_once_with("coins")
        assert len(result) == 3
        assert isinstance(result[0], CoinCategory)
        assert result[0].name == "Criptomonedas"
        assert len(result[0].coins) == 1
        assert isinstance(result[0].coins[0], Coin)
        assert result[0].coins[0].tick == "BTC"
        assert result[1].name == "Bank"
        assert result[1].coins[0].tick == "ZELLE"
        assert result[2].name == "Cash"
        assert result[2].coins == []
