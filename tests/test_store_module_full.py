from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.store import StoreModule as AsyncStoreModule
from qvapay._sync.modules.store import StoreModule as SyncStoreModule
from qvapay.models.purchased_product import PurchasedProduct

PHONE_PACKAGE = {"id": 20, "name": "NAUTA PLUS", "price": 8.59}
VISA_SERVICE = {"id": "34", "uuid": "visa-123", "name": "Tarjeta VISA"}
GIFT_CARD = {"id": 27, "uuid": "gift-123", "name": "Amazon US"}
GIFT_CARD_DETAIL = {"message": "details", "data": GIFT_CARD}
GIFT_CARD_PURCHASE = {"message": "ok", "data": {"status": "pending"}}
PURCHASED_DETAIL = {
    "id": 6003,
    "service_id": 2,
    "service_data": '{"name":"Pedro"}',
    "notes": "",
    "status": "pending",
    "amount": "5.00",
    "transaction_id": 767745,
    "notified": "no",
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


class TestAsyncStoreModuleFull:
    @pytest.mark.anyio
    async def test_submodules_and_detail(self):
        http = AsyncMock()
        http.get.side_effect = [
            _mock_response(
                {"phone_packages": [PHONE_PACKAGE]},
                url="https://api.qvapay.com/store/phone_package",
            ),
            _mock_response(
                {"visaCardService": VISA_SERVICE},
                url="https://api.qvapay.com/store/visa_card",
            ),
            _mock_response(
                {"data": [GIFT_CARD]},
                url="https://api.qvapay.com/store/gift-card",
            ),
            _mock_response(
                GIFT_CARD_DETAIL,
                url="https://api.qvapay.com/store/gift-card/gift-123",
            ),
            _mock_response(
                {"data": PURCHASED_DETAIL},
                url="https://api.qvapay.com/store/my/6003",
            ),
        ]
        http.post.side_effect = [
            _mock_response(
                {}, method="POST", url="https://api.qvapay.com/store/phone_package"
            ),
            _mock_response(
                {}, method="POST", url="https://api.qvapay.com/store/visa_card"
            ),
            _mock_response(
                GIFT_CARD_PURCHASE,
                method="POST",
                url="https://api.qvapay.com/store/gift-card/gift-123",
            ),
        ]
        module = AsyncStoreModule(http)

        phone_packages = await module.phone_package.list()
        phone_purchase = await module.phone_package.purchase(phone="5355")
        debit_card = await module.debit_card.list()
        debit_purchase = await module.debit_card.purchase(amount=50)
        catalog = await module.gift_card.catalog()
        detail = await module.gift_card.get("gift-123")
        purchase = await module.gift_card.purchase("gift-123", code="AMAZON")
        purchased_detail = await module.get_purchased("6003")

        assert phone_packages == [PHONE_PACKAGE]
        assert phone_purchase == {}
        assert debit_card == VISA_SERVICE
        assert debit_purchase == {}
        assert catalog == [GIFT_CARD]
        assert detail == GIFT_CARD_DETAIL
        assert purchase == GIFT_CARD_PURCHASE
        assert isinstance(purchased_detail, PurchasedProduct)
        assert purchased_detail.amount == 5.0
        http.get.assert_any_call("store/phone_package")
        http.get.assert_any_call("store/visa_card")
        http.get.assert_any_call("store/gift-card")
        http.get.assert_any_call("store/gift-card/gift-123")
        http.get.assert_any_call("store/my/6003")
        http.post.assert_any_call("store/phone_package", json={"phone": "5355"})
        http.post.assert_any_call("store/visa_card", json={"amount": 50})
        http.post.assert_any_call("store/gift-card/gift-123", json={"code": "AMAZON"})


class TestSyncStoreModuleFull:
    def test_submodules_and_detail(self):
        http = MagicMock()
        http.get.side_effect = [
            _mock_response(
                {"phone_packages": [PHONE_PACKAGE]},
                url="https://api.qvapay.com/store/phone_package",
            ),
            _mock_response(
                {"visaCardService": VISA_SERVICE},
                url="https://api.qvapay.com/store/visa_card",
            ),
            _mock_response(
                {"data": [GIFT_CARD]},
                url="https://api.qvapay.com/store/gift-card",
            ),
            _mock_response(
                GIFT_CARD_DETAIL,
                url="https://api.qvapay.com/store/gift-card/gift-123",
            ),
            _mock_response(
                {"data": PURCHASED_DETAIL},
                url="https://api.qvapay.com/store/my/6003",
            ),
        ]
        http.post.side_effect = [
            _mock_response(
                {}, method="POST", url="https://api.qvapay.com/store/phone_package"
            ),
            _mock_response(
                {}, method="POST", url="https://api.qvapay.com/store/visa_card"
            ),
            _mock_response(
                GIFT_CARD_PURCHASE,
                method="POST",
                url="https://api.qvapay.com/store/gift-card/gift-123",
            ),
        ]
        module = SyncStoreModule(http)

        phone_packages = module.phone_package.list()
        phone_purchase = module.phone_package.purchase(phone="5355")
        debit_card = module.debit_card.list()
        debit_purchase = module.debit_card.purchase(amount=50)
        catalog = module.gift_card.catalog()
        detail = module.gift_card.get("gift-123")
        purchase = module.gift_card.purchase("gift-123", code="AMAZON")
        purchased_detail = module.get_purchased("6003")

        assert phone_packages == [PHONE_PACKAGE]
        assert phone_purchase == {}
        assert debit_card == VISA_SERVICE
        assert debit_purchase == {}
        assert catalog == [GIFT_CARD]
        assert detail == GIFT_CARD_DETAIL
        assert purchase == GIFT_CARD_PURCHASE
        assert isinstance(purchased_detail, PurchasedProduct)
        assert purchased_detail.amount == 5.0
        http.get.assert_any_call("store/phone_package")
        http.get.assert_any_call("store/visa_card")
        http.get.assert_any_call("store/gift-card")
        http.get.assert_any_call("store/gift-card/gift-123")
        http.get.assert_any_call("store/my/6003")
        http.post.assert_any_call("store/phone_package", json={"phone": "5355"})
        http.post.assert_any_call("store/visa_card", json={"amount": 50})
        http.post.assert_any_call("store/gift-card/gift-123", json={"code": "AMAZON"})
