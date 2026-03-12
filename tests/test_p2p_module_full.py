from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.p2p import P2PModule as AsyncP2PModule
from qvapay._sync.modules.p2p import P2PModule as SyncP2PModule
from qvapay.models.p2p import P2PMessage, P2POffer

P2P_OFFER = {
    "uuid": "949780ed-7303-4a34-b8c3-2d55d802c75d",
    "coin": "ETECSA",
    "amount": "5.00",
    "receive": "650.000000000000",
    "type": "buy",
    "status": "open",
}

P2P_MESSAGE = {
    "uuid": "msg-123",
    "message": "Hola",
    "sender": "seller",
    "created_at": "2025-01-01T00:00:00.000Z",
}

AVERAGE_DATA = {"coin": "BTC", "average": 100000}
AVERAGES_DATA = {"BTC": 100000, "USDT": 1}
TOTALS_DATA = {"buy": 199, "sell": 143}
ACTION_DATA = {"message": "ok"}


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


class TestAsyncP2PModuleFull:
    @pytest.mark.anyio
    async def test_chat_and_reads(self):
        http = AsyncMock()
        http.get.side_effect = [
            _mock_response([P2P_MESSAGE], url="https://api.qvapay.com/p2p/offer/chat"),
            _mock_response(AVERAGE_DATA, url="https://api.qvapay.com/p2p/average"),
            _mock_response(AVERAGES_DATA, url="https://api.qvapay.com/p2p/averages"),
            _mock_response(
                TOTALS_DATA, url="https://api.qvapay.com/p2p/get_total_operations"
            ),
            _mock_response([P2P_OFFER]),
            _mock_response(P2P_OFFER, url="https://api.qvapay.com/p2p/offer"),
            _mock_response(P2P_OFFER, url="https://api.qvapay.com/p2p/offer/pub"),
        ]
        http.post.side_effect = [
            _mock_response(
                P2P_MESSAGE, method="POST", url="https://api.qvapay.com/p2p/offer/chat"
            ),
        ]
        module = AsyncP2PModule(http)

        messages = await module.chat.get("offer")
        sent = await module.chat.send("offer", "Hola")
        average = await module.average("btc")
        averages = await module.averages()
        totals = await module.total_public_open_ops()
        offers = await module.get_offers(type="buy", vip=True, coin=None)
        offer = await module.get_offer("offer")
        public_offer = await module.get_offer_public("offer")

        assert isinstance(messages[0], P2PMessage)
        assert isinstance(sent, P2PMessage)
        assert average == AVERAGE_DATA
        assert averages == AVERAGES_DATA
        assert totals == TOTALS_DATA
        assert isinstance(offers[0], P2POffer)
        assert offers[0].price == 650.0
        assert isinstance(offer, P2POffer)
        assert isinstance(public_offer, P2POffer)
        http.get.assert_any_call("p2p/offer/chat")
        http.post.assert_any_call(
            "p2p/offer/chat",
            json={"message": "Hola"},
        )
        http.get.assert_any_call("p2p/average", params={"coin": "btc"})
        http.get.assert_any_call("p2p/averages")
        http.get.assert_any_call("p2p/get_total_operations")
        http.get.assert_any_call(
            "p2p",
            params={"type": "buy", "vip": "true"},
        )
        http.get.assert_any_call("p2p/offer")
        http.get.assert_any_call("p2p/offer/pub")

    @pytest.mark.anyio
    async def test_write_operations(self):
        http = AsyncMock()
        http.post.side_effect = [
            _mock_response(
                P2P_OFFER, method="POST", url="https://api.qvapay.com/p2p/create"
            ),
            _mock_response(
                P2P_OFFER, method="POST", url="https://api.qvapay.com/p2p/offer/edit"
            ),
            _mock_response(
                ACTION_DATA, method="POST", url="https://api.qvapay.com/p2p/offer/apply"
            ),
            _mock_response(
                ACTION_DATA, method="POST", url="https://api.qvapay.com/p2p/offer/paid"
            ),
            _mock_response(
                ACTION_DATA,
                method="POST",
                url="https://api.qvapay.com/p2p/offer/received",
            ),
            _mock_response(
                ACTION_DATA,
                method="POST",
                url="https://api.qvapay.com/p2p/offer/cancel",
            ),
            _mock_response(
                ACTION_DATA, method="POST", url="https://api.qvapay.com/p2p/offer/rate"
            ),
        ]
        module = AsyncP2PModule(http)

        created = await module.create_offer(type="sell", coin="USDT")
        edited = await module.edit_offer("offer", amount=50)
        applied = await module.apply("offer")
        paid = await module.mark_paid("offer")
        received = await module.confirm_received("offer")
        cancelled = await module.cancel("offer")
        rated = await module.rate("offer", 5)

        assert isinstance(created, P2POffer)
        assert isinstance(edited, P2POffer)
        assert applied == ACTION_DATA
        assert paid == ACTION_DATA
        assert received == ACTION_DATA
        assert cancelled == ACTION_DATA
        assert rated == ACTION_DATA
        http.post.assert_any_call("p2p/create", json={"type": "sell", "coin": "USDT"})
        http.post.assert_any_call("p2p/offer/edit", json={"amount": 50})
        http.post.assert_any_call("p2p/offer/apply")
        http.post.assert_any_call("p2p/offer/paid")
        http.post.assert_any_call("p2p/offer/received")
        http.post.assert_any_call("p2p/offer/cancel")
        http.post.assert_any_call("p2p/offer/rate", json={"rating": 5})


class TestSyncP2PModuleFull:
    def test_chat_and_reads(self):
        http = MagicMock()
        http.get.side_effect = [
            _mock_response([P2P_MESSAGE], url="https://api.qvapay.com/p2p/offer/chat"),
            _mock_response(AVERAGE_DATA, url="https://api.qvapay.com/p2p/average"),
            _mock_response(AVERAGES_DATA, url="https://api.qvapay.com/p2p/averages"),
            _mock_response(
                TOTALS_DATA, url="https://api.qvapay.com/p2p/get_total_operations"
            ),
            _mock_response([P2P_OFFER]),
            _mock_response(P2P_OFFER, url="https://api.qvapay.com/p2p/offer"),
            _mock_response(P2P_OFFER, url="https://api.qvapay.com/p2p/offer/pub"),
        ]
        http.post.side_effect = [
            _mock_response(
                P2P_MESSAGE, method="POST", url="https://api.qvapay.com/p2p/offer/chat"
            ),
        ]
        module = SyncP2PModule(http)

        messages = module.chat.get("offer")
        sent = module.chat.send("offer", "Hola")
        average = module.average("btc")
        averages = module.averages()
        totals = module.total_public_open_ops()
        offers = module.get_offers(type="buy", vip=True, coin=None)
        offer = module.get_offer("offer")
        public_offer = module.get_offer_public("offer")

        assert isinstance(messages[0], P2PMessage)
        assert isinstance(sent, P2PMessage)
        assert average == AVERAGE_DATA
        assert averages == AVERAGES_DATA
        assert totals == TOTALS_DATA
        assert isinstance(offers[0], P2POffer)
        assert offers[0].price == 650.0
        assert isinstance(offer, P2POffer)
        assert isinstance(public_offer, P2POffer)
        http.get.assert_any_call("p2p/offer/chat")
        http.post.assert_any_call(
            "p2p/offer/chat",
            json={"message": "Hola"},
        )
        http.get.assert_any_call("p2p/average", params={"coin": "btc"})
        http.get.assert_any_call("p2p/averages")
        http.get.assert_any_call("p2p/get_total_operations")
        http.get.assert_any_call(
            "p2p",
            params={"type": "buy", "vip": "true"},
        )
        http.get.assert_any_call("p2p/offer")
        http.get.assert_any_call("p2p/offer/pub")

    def test_write_operations(self):
        http = MagicMock()
        http.post.side_effect = [
            _mock_response(
                P2P_OFFER, method="POST", url="https://api.qvapay.com/p2p/create"
            ),
            _mock_response(
                P2P_OFFER, method="POST", url="https://api.qvapay.com/p2p/offer/edit"
            ),
            _mock_response(
                ACTION_DATA, method="POST", url="https://api.qvapay.com/p2p/offer/apply"
            ),
            _mock_response(
                ACTION_DATA, method="POST", url="https://api.qvapay.com/p2p/offer/paid"
            ),
            _mock_response(
                ACTION_DATA,
                method="POST",
                url="https://api.qvapay.com/p2p/offer/received",
            ),
            _mock_response(
                ACTION_DATA,
                method="POST",
                url="https://api.qvapay.com/p2p/offer/cancel",
            ),
            _mock_response(
                ACTION_DATA, method="POST", url="https://api.qvapay.com/p2p/offer/rate"
            ),
        ]
        module = SyncP2PModule(http)

        created = module.create_offer(type="sell", coin="USDT")
        edited = module.edit_offer("offer", amount=50)
        applied = module.apply("offer")
        paid = module.mark_paid("offer")
        received = module.confirm_received("offer")
        cancelled = module.cancel("offer")
        rated = module.rate("offer", 5)

        assert isinstance(created, P2POffer)
        assert isinstance(edited, P2POffer)
        assert applied == ACTION_DATA
        assert paid == ACTION_DATA
        assert received == ACTION_DATA
        assert cancelled == ACTION_DATA
        assert rated == ACTION_DATA
        http.post.assert_any_call("p2p/create", json={"type": "sell", "coin": "USDT"})
        http.post.assert_any_call("p2p/offer/edit", json={"amount": 50})
        http.post.assert_any_call("p2p/offer/apply")
        http.post.assert_any_call("p2p/offer/paid")
        http.post.assert_any_call("p2p/offer/received")
        http.post.assert_any_call("p2p/offer/cancel")
        http.post.assert_any_call("p2p/offer/rate", json={"rating": 5})
