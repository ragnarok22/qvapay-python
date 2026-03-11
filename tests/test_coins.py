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

COIN_V2_DATA = {
    "id": "78",
    "name": "AXS (BSC)",
    "tick": "AXS",
    "min_in": "1",
    "fee_in": "1",
    "min_out": "30",
    "fee_out": "2",
    "enabled_in": True,
    "enabled_out": True,
    "enabled_p2p": True,
    "coins_categories_id": "1",
    "price": "2.213403886960948",
    "logo": "axs",
    "network": "BSC",
}

COIN_V2_NO_NETWORK = {
    "id": "1",
    "name": "Bitcoin",
    "tick": "BTC",
    "min_in": "20",
    "fee_in": "1",
    "min_out": "60",
    "fee_out": "7.5",
    "enabled_in": True,
    "enabled_out": True,
    "enabled_p2p": True,
    "coins_categories_id": "1",
    "price": "76329.15494707902",
    "logo": "btc",
    "network": None,
}

COIN_DETAIL_DATA = {
    "id": 1,
    "coins_categories_id": 1,
    "name": "BitCoin",
    "logo": "btc",
    "tick": "BTC",
    "fee_in": "0.00",
    "fee_out": "7.50",
    "min_in": "30.00",
    "min_out": "20.00",
    "max_in": 1000,
    "max_out": 1000,
    "working_data": '[{"name": "Wallet", "type": "text"}]',
    "enabled_in": 1,
    "enabled_out": 1,
    "enabled_p2p": 1,
    "price": "21698.968770779000000000",
    "coin_category": {
        "id": 1,
        "name": "Criptomonedas",
        "logo": "crypto",
    },
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
LIST_V2_RESPONSE = [COIN_V2_DATA, COIN_V2_NO_NETWORK]


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

    def test_from_json_v2_with_network(self):
        coin = Coin.from_json(COIN_V2_DATA)
        assert coin.id == "78"
        assert coin.name == "AXS (BSC)"
        assert coin.tick == "AXS"
        assert coin.network == "BSC"
        assert coin.enabled_in is True
        assert coin.enabled_out is True
        assert coin.enabled_p2p is True

    def test_from_json_v2_null_network(self):
        coin = Coin.from_json(COIN_V2_NO_NETWORK)
        assert coin.id == "1"
        assert coin.network is None

    def test_from_json_detail_with_category(self):
        coin = Coin.from_json(COIN_DETAIL_DATA)
        assert coin.id == "1"
        assert coin.name == "BitCoin"
        assert coin.max_in == 1000.0
        assert coin.max_out == 1000.0
        assert isinstance(coin.max_in, float)
        assert isinstance(coin.max_out, float)
        assert coin.coin_category is not None
        assert isinstance(coin.coin_category, CoinCategory)
        assert coin.coin_category.id == 1
        assert coin.coin_category.name == "Criptomonedas"
        assert coin.coin_category.logo == "crypto"
        assert coin.coin_category.coins == []

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
        assert coin.max_in is None
        assert coin.max_out is None
        assert coin.network is None
        assert coin.coin_category is None
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


class TestAsyncListV2:
    @pytest.mark.anyio
    async def test_list_v2_no_filters(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            result = await async_coins.list_v2()

        mock_client.get.assert_called_once_with("coins/v2", params={})
        assert len(result) == 2
        assert isinstance(result[0], Coin)
        assert result[0].tick == "AXS"
        assert result[0].network == "BSC"
        assert result[1].tick == "BTC"
        assert result[1].network is None

    @pytest.mark.anyio
    async def test_list_v2_with_enabled_in(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            await async_coins.list_v2(enabled_in=True)

        mock_client.get.assert_called_once_with(
            "coins/v2", params={"enabled_in": "true"}
        )

    @pytest.mark.anyio
    async def test_list_v2_with_all_filters(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            await async_coins.list_v2(
                enabled_in=True, enabled_out=False, enabled_p2p=True
            )

        mock_client.get.assert_called_once_with(
            "coins/v2",
            params={
                "enabled_in": "true",
                "enabled_out": "false",
                "enabled_p2p": "true",
            },
        )

    @pytest.mark.anyio
    async def test_list_v2_omits_none_filters(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            await async_coins.list_v2(enabled_out=True)

        params = mock_client.get.call_args[1]["params"]
        assert params == {"enabled_out": "true"}
        assert "enabled_in" not in params
        assert "enabled_p2p" not in params


class TestAsyncGet:
    @pytest.mark.anyio
    async def test_get(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(COIN_DETAIL_DATA)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            coin = await async_coins.get(1)

        mock_client.get.assert_called_once_with("coins/1")
        assert isinstance(coin, Coin)
        assert coin.tick == "BTC"
        assert coin.max_in == 1000.0
        assert coin.max_out == 1000.0
        assert isinstance(coin.coin_category, CoinCategory)
        assert coin.coin_category.name == "Criptomonedas"


class TestAsyncPriceHistory:
    @pytest.mark.anyio
    async def test_price_history(self):
        history_data = [{"date": "2022-07-08", "price": "21698.97"}]
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response(history_data)
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            result = await async_coins.price_history("BTC")

        mock_client.get.assert_called_once_with(
            "coins/price-history/BTC", params={"timeframe": "24H"}
        )
        assert result == history_data

    @pytest.mark.anyio
    async def test_price_history_custom_timeframe(self):
        mock_client = AsyncMock()
        mock_client.get.return_value = _mock_response([])
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = False

        with patch("qvapay._async.coins._client", return_value=mock_client):
            await async_coins.price_history("ETH", timeframe="7D")

        mock_client.get.assert_called_once_with(
            "coins/price-history/ETH", params={"timeframe": "7D"}
        )


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


class TestSyncListV2:
    def test_list_v2_no_filters(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            result = sync_coins.list_v2()

        mock_client.get.assert_called_once_with("coins/v2", params={})
        assert len(result) == 2
        assert isinstance(result[0], Coin)
        assert result[0].tick == "AXS"
        assert result[0].network == "BSC"
        assert result[1].tick == "BTC"
        assert result[1].network is None

    def test_list_v2_with_enabled_in(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            sync_coins.list_v2(enabled_in=True)

        mock_client.get.assert_called_once_with(
            "coins/v2", params={"enabled_in": "true"}
        )

    def test_list_v2_with_all_filters(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            sync_coins.list_v2(enabled_in=True, enabled_out=False, enabled_p2p=True)

        mock_client.get.assert_called_once_with(
            "coins/v2",
            params={
                "enabled_in": "true",
                "enabled_out": "false",
                "enabled_p2p": "true",
            },
        )

    def test_list_v2_omits_none_filters(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(LIST_V2_RESPONSE)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            sync_coins.list_v2(enabled_out=True)

        params = mock_client.get.call_args[1]["params"]
        assert params == {"enabled_out": "true"}
        assert "enabled_in" not in params
        assert "enabled_p2p" not in params


class TestSyncGet:
    def test_get(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(COIN_DETAIL_DATA)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            coin = sync_coins.get(1)

        mock_client.get.assert_called_once_with("coins/1")
        assert isinstance(coin, Coin)
        assert coin.tick == "BTC"
        assert coin.max_in == 1000.0
        assert coin.max_out == 1000.0
        assert isinstance(coin.coin_category, CoinCategory)
        assert coin.coin_category.name == "Criptomonedas"


class TestSyncPriceHistory:
    def test_price_history(self):
        history_data = [{"date": "2022-07-08", "price": "21698.97"}]
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response(history_data)
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            result = sync_coins.price_history("BTC")

        mock_client.get.assert_called_once_with(
            "coins/price-history/BTC", params={"timeframe": "24H"}
        )
        assert result == history_data

    def test_price_history_custom_timeframe(self):
        mock_client = MagicMock()
        mock_client.get.return_value = _mock_response([])
        mock_client.__enter__.return_value = mock_client
        mock_client.__exit__.return_value = False

        with patch("qvapay._sync.coins._client", return_value=mock_client):
            sync_coins.price_history("ETH", timeframe="7D")

        mock_client.get.assert_called_once_with(
            "coins/price-history/ETH", params={"timeframe": "7D"}
        )
