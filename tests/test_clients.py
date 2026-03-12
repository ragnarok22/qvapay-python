from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from qvapay._async.client import AsyncQvaPayClient
from qvapay._sync.client import SyncQvaPayClient
from qvapay.http import BASE_URL


class TestAsyncQvaPayClient:
    def test_initializes_http_and_modules(self):
        http = MagicMock()
        http.aclose = AsyncMock()

        with patch("qvapay._async.client.AsyncClient", return_value=http) as client_cls:
            with patch("qvapay._async.client.AppModule", return_value="app") as app_cls:
                with patch(
                    "qvapay._async.client.TransactionsModule",
                    return_value="transactions",
                ) as tx_cls:
                    with patch(
                        "qvapay._async.client.WithdrawModule",
                        return_value="withdraw",
                    ) as withdraw_cls:
                        with patch(
                            "qvapay._async.client.UserModule",
                            return_value="user",
                        ) as user_cls:
                            with patch(
                                "qvapay._async.client.P2PModule",
                                return_value="p2p",
                            ) as p2p_cls:
                                with patch(
                                    "qvapay._async.client.PaymentLinksModule",
                                    return_value="payment_links",
                                ) as links_cls:
                                    with patch(
                                        "qvapay._async.client.StoreModule",
                                        return_value="store",
                                    ) as store_cls:
                                        with patch(
                                            "qvapay._async.client.TopupModule",
                                            return_value="topup",
                                        ) as topup_cls:
                                            client = AsyncQvaPayClient("token123")

        kwargs = client_cls.call_args.kwargs
        assert kwargs["base_url"] == BASE_URL
        assert kwargs["headers"] == {"Authorization": "Bearer token123"}
        assert kwargs["follow_redirects"] is True
        app_cls.assert_called_once_with(http)
        tx_cls.assert_called_once_with(http)
        withdraw_cls.assert_called_once_with(http)
        user_cls.assert_called_once_with(http)
        p2p_cls.assert_called_once_with(http)
        links_cls.assert_called_once_with(http)
        store_cls.assert_called_once_with(http)
        topup_cls.assert_called_once_with(http)
        assert client.app == "app"
        assert client.transactions == "transactions"
        assert client.withdraw == "withdraw"
        assert client.user == "user"
        assert client.p2p == "p2p"
        assert client.payment_links == "payment_links"
        assert client.store == "store"
        assert client.topup == "topup"

    @pytest.mark.anyio
    async def test_context_manager_and_close(self):
        http = MagicMock()
        http.aclose = AsyncMock()

        with patch("qvapay._async.client.AsyncClient", return_value=http):
            client = AsyncQvaPayClient("token123")

        assert await client.__aenter__() is client
        await client.__aexit__(None, None, None)
        http.aclose.assert_awaited_once()


class TestSyncQvaPayClient:
    def test_initializes_http_and_modules(self):
        http = MagicMock()

        with patch("qvapay._sync.client.SyncClient", return_value=http) as client_cls:
            with patch("qvapay._sync.client.AppModule", return_value="app") as app_cls:
                with patch(
                    "qvapay._sync.client.TransactionsModule",
                    return_value="transactions",
                ) as tx_cls:
                    with patch(
                        "qvapay._sync.client.WithdrawModule",
                        return_value="withdraw",
                    ) as withdraw_cls:
                        with patch(
                            "qvapay._sync.client.UserModule",
                            return_value="user",
                        ) as user_cls:
                            with patch(
                                "qvapay._sync.client.P2PModule",
                                return_value="p2p",
                            ) as p2p_cls:
                                with patch(
                                    "qvapay._sync.client.PaymentLinksModule",
                                    return_value="payment_links",
                                ) as links_cls:
                                    with patch(
                                        "qvapay._sync.client.StoreModule",
                                        return_value="store",
                                    ) as store_cls:
                                        with patch(
                                            "qvapay._sync.client.TopupModule",
                                            return_value="topup",
                                        ) as topup_cls:
                                            client = SyncQvaPayClient("token123")

        kwargs = client_cls.call_args.kwargs
        assert kwargs["base_url"] == BASE_URL
        assert kwargs["headers"] == {"Authorization": "Bearer token123"}
        assert kwargs["follow_redirects"] is True
        app_cls.assert_called_once_with(http)
        tx_cls.assert_called_once_with(http)
        withdraw_cls.assert_called_once_with(http)
        user_cls.assert_called_once_with(http)
        p2p_cls.assert_called_once_with(http)
        links_cls.assert_called_once_with(http)
        store_cls.assert_called_once_with(http)
        topup_cls.assert_called_once_with(http)
        assert client.app == "app"
        assert client.transactions == "transactions"
        assert client.withdraw == "withdraw"
        assert client.user == "user"
        assert client.p2p == "p2p"
        assert client.payment_links == "payment_links"
        assert client.store == "store"
        assert client.topup == "topup"

    def test_context_manager_and_close(self):
        http = MagicMock()

        with patch("qvapay._sync.client.SyncClient", return_value=http):
            client = SyncQvaPayClient("token123")

        assert client.__enter__() is client
        client.__exit__(None, None, None)
        http.aclose.assert_called_once_with()
