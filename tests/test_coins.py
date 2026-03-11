from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from qvapay._async import coins as async_coins
from qvapay._sync import coins as sync_coins
from qvapay.models.coin import Coin, CoinCategory

COIN_DATA = {
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

COIN_DATA_2 = {
    "id": 6,
    "coins_categories_id": 1,
    "name": "USDT TRC20",
    "logo": "usdt",
    "tick": "USDT",
    "fee_in": "1.00",
    "fee_out": "1.50",
    "min_in": "10.00",
    "min_out": "20.00",
    "working_data": '[{"name": "Wallet", "type": "text"}]',
    "enabled_in": 1,
    "enabled_out": 1,
    "enabled_p2p": 1,
    "price": "0.999374298557880000",
    "created_at": None,
    "updated_at": "2022-07-08T17:10:02.000000Z",
}

COIN_DISABLED = {
    "id": 3,
    "coins_categories_id": 1,
    "name": "Ethereum",
    "logo": "eth",
    "tick": "ETH",
    "fee_in": "1.00",
    "fee_out": "10.00",
    "min_in": "80.00",
    "min_out": "80.00",
    "working_data": '[{"name": "Wallet", "type": "text"}]',
    "enabled_in": 0,
    "enabled_out": 1,
    "enabled_p2p": 1,
    "price": "1221.728429324000000000",
    "created_at": None,
    "updated_at": "2022-07-08T17:10:01.000000Z",
}

CATEGORY_CRYPTO = {
    "id": 1,
    "name": "Criptomonedas",
    "logo": "crypto",
    "coins": [COIN_DATA, COIN_DATA_2],
}

CATEGORY_EMPTY = {
    "id": 3,
    "name": "Cash",
    "logo": "cash",
    "coins": [],
}

LIST_RESPONSE = [CATEGORY_CRYPTO, CATEGORY_EMPTY]


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


# -- Model tests -------------------------------------------------------------


class TestCoin:
    def test_from_json(self):
        coin = Coin.from_json(COIN_DATA)
        assert coin.id == "1"
        assert coin.name == "BitCoin"
        assert coin.logo == "btc"
        assert coin.tick == "BTC"
        assert coin.price == "21698.968770779000000000"
        assert coin.fee_in == "0.00"
        assert coin.fee_out == "7.50"
        assert coin.min_in == "30.00"
        assert coin.min_out == "20.00"
        assert coin.enabled_in is True
        assert coin.enabled_out is True
        assert coin.enabled_p2p is True
        assert coin.coins_categories_id == 1
        assert coin.working_data == '[{"name": "Wallet", "type": "text"}]'
        assert coin.created_at is None
        assert coin.updated_at == "2022-07-08T17:10:01.000000Z"

    def test_from_json_disabled_coin(self):
        coin = Coin.from_json(COIN_DISABLED)
        assert coin.enabled_in is False
        assert coin.enabled_out is True
        assert coin.name == "Ethereum"

    def test_from_json_minimal(self):
        minimal = {
            "id": 99,
            "name": "TestCoin",
            "logo": "test",
            "tick": "TST",
            "price": "1.00",
            "enabled_in": 0,
            "enabled_out": 0,
            "enabled_p2p": 0,
            "fee_in": "0.00",
            "fee_out": "0.00",
            "min_in": "0.00",
            "min_out": "0.00",
        }
        coin = Coin.from_json(minimal)
        assert coin.id == "99"
        assert coin.coins_categories_id is None
        assert coin.working_data is None
        assert coin.created_at is None
        assert coin.updated_at is None

    def test_id_coerced_to_string(self):
        coin = Coin.from_json(COIN_DATA)
        assert isinstance(coin.id, str)

    def test_enabled_flags_coerced_to_bool(self):
        coin = Coin.from_json(COIN_DATA)
        assert isinstance(coin.enabled_in, bool)
        assert isinstance(coin.enabled_out, bool)
        assert isinstance(coin.enabled_p2p, bool)


class TestCoinCategory:
    def test_from_json(self):
        cat = CoinCategory.from_json(CATEGORY_CRYPTO)
        assert cat.id == 1
        assert cat.name == "Criptomonedas"
        assert cat.logo == "crypto"
        assert len(cat.coins) == 2
        assert isinstance(cat.coins[0], Coin)
        assert cat.coins[0].tick == "BTC"
        assert cat.coins[1].tick == "USDT"

    def test_from_json_empty_coins(self):
        cat = CoinCategory.from_json(CATEGORY_EMPTY)
        assert cat.id == 3
        assert cat.name == "Cash"
        assert cat.coins == []

    def test_from_json_uppercase_coins_key(self):
        data = {
            "id": 1,
            "name": "Crypto",
            "logo": "crypto",
            "Coins": [COIN_DATA],
        }
        cat = CoinCategory.from_json(data)
        assert len(cat.coins) == 1
        assert cat.coins[0].tick == "BTC"


# -- Async module tests ------------------------------------------------------


class TestAsyncList:
    @pytest.mark.anyio
    async def test_list(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(LIST_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            result = await async_coins.list()

        mock_client.get.assert_called_once_with("coins")
        assert len(result) == 2
        assert isinstance(result[0], CoinCategory)
        assert result[0].name == "Criptomonedas"
        assert len(result[0].coins) == 2
        assert result[1].coins == []

    @pytest.mark.anyio
    async def test_list_v2(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(LIST_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            result = await async_coins.list_v2()

        mock_client.get.assert_called_once_with("v2/coins")
        assert len(result) == 2


class TestAsyncGet:
    @pytest.mark.anyio
    async def test_get(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(COIN_DATA)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            coin = await async_coins.get(1)

        mock_client.get.assert_called_once_with("coins/1")
        assert isinstance(coin, Coin)
        assert coin.tick == "BTC"


class TestAsyncHistory:
    @pytest.mark.anyio
    async def test_history(self):
        history_data = [{"date": "2022-07-08", "price": "21698.97"}]
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(history_data)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            result = await async_coins.history()

        mock_client.get.assert_called_once_with("coins/history")
        assert result == history_data


# -- Sync module tests -------------------------------------------------------


class TestSyncList:
    def test_list(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            result = sync_coins.list()

        mock_client.get.assert_called_once_with("coins")
        assert len(result) == 2
        assert isinstance(result[0], CoinCategory)
        assert result[0].name == "Criptomonedas"
        assert len(result[0].coins) == 2
        assert result[1].coins == []

    def test_list_v2(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            result = sync_coins.list_v2()

        mock_client.get.assert_called_once_with("v2/coins")
        assert len(result) == 2


class TestSyncGet:
    def test_get(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(COIN_DATA)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            coin = sync_coins.get(1)

        mock_client.get.assert_called_once_with("coins/1")
        assert isinstance(coin, Coin)
        assert coin.tick == "BTC"


class TestSyncHistory:
    def test_history(self):
        history_data = [{"date": "2022-07-08", "price": "21698.97"}]
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(history_data)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            result = sync_coins.history()

        mock_client.get.assert_called_once_with("coins/history")
        assert result == history_data
