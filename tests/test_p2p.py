from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.p2p import P2PModule as AsyncP2PModule
from qvapay._sync.modules.p2p import P2PModule as SyncP2PModule
from qvapay.models.p2p import P2POffer

P2P_OFFER = {
    "uuid": "1d8ad0fa-d7ad-43d9-8d67-4669321a45f6",
    "coin": "BANK_CUP",
    "amount": "100.00",
    "receive": "16000.000000000000",
    "type": "sell",
    "status": "open",
}

P2P_STATS = {
    "average": 392.40818576803605,
    "average_buy": 395.685442499371,
    "average_sell": 398.3642714657489,
}


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/p2p",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


class TestAsyncP2PModule:
    @pytest.mark.anyio
    async def test_get_my_offers_uses_query_flag_and_unwraps_data(self):
        http = AsyncMock()
        http.get.return_value = _mock_response({"data": [P2P_OFFER]})
        module = AsyncP2PModule(http)

        offers = await module.get_my_offers()

        http.get.assert_called_once_with("p2p", params={"my": "true"})
        assert len(offers) == 1
        assert isinstance(offers[0], P2POffer)
        assert offers[0].price == 16000.0

    @pytest.mark.anyio
    async def test_completed_pairs_average_returns_stats_payload(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(
            P2P_STATS,
            url="https://api.qvapay.com/p2p/completed_pairs_average",
        )
        module = AsyncP2PModule(http)

        stats = await module.completed_pairs_average("bank_cup")

        http.get.assert_called_once_with(
            "p2p/completed_pairs_average",
            params={"coin": "BANK_CUP"},
        )
        assert stats == P2P_STATS


class TestSyncP2PModule:
    def test_get_my_offers_uses_query_flag_and_unwraps_data(self):
        http = MagicMock()
        http.get.return_value = _mock_response({"data": [P2P_OFFER]})
        module = SyncP2PModule(http)

        offers = module.get_my_offers()

        http.get.assert_called_once_with("p2p", params={"my": "true"})
        assert len(offers) == 1
        assert isinstance(offers[0], P2POffer)
        assert offers[0].price == 16000.0

    def test_completed_pairs_average_returns_stats_payload(self):
        http = MagicMock()
        http.get.return_value = _mock_response(
            P2P_STATS,
            url="https://api.qvapay.com/p2p/completed_pairs_average",
        )
        module = SyncP2PModule(http)

        stats = module.completed_pairs_average("bank_cup")

        http.get.assert_called_once_with(
            "p2p/completed_pairs_average",
            params={"coin": "BANK_CUP"},
        )
        assert stats == P2P_STATS
