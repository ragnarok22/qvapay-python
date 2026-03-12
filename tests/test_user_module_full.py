from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.user import UserModule as AsyncUserModule
from qvapay._sync.modules.user import UserModule as SyncUserModule
from qvapay.models.contact import Contact
from qvapay.models.domain import Domain
from qvapay.models.payment_link import PaymentLink
from qvapay.models.payment_method import PaymentMethod
from qvapay.models.user import User

USER_DATA = {
    "uuid": "12b1e145-82ce-480a-b5c6-1a681a125f0a",
    "username": "skymind",
    "name": "SkyMind",
    "lastname": "Payments",
    "email": "ceo@skymind.ltd",
    "bio": "Soluciones Fintech a la medida.",
    "image": "profiles/user.png",
    "cover": "covers/user.jpg",
    "balance": "90.59",
    "pending_balance": "0",
    "satoshis": 2424,
    "createdAt": "2024-01-28T23:24:54.000Z",
    "updatedAt": "2025-07-19T16:49:01.000Z",
    "phone": "+17867918868",
    "phone_verified": True,
    "telegram": "",
    "twitter": None,
    "kyc": True,
    "vip": True,
    "golden_check": False,
    "pin": 1111,
    "last_seen": "2025-07-19T16:49:01.000Z",
    "telegram_id": "7427512552",
    "role": "admin",
    "p2p_enabled": True,
}

PAYMENT_METHOD_DATA = {
    "uuid": "pm-123",
    "name": "Primary wallet",
    "details": '{"Wallet":"abc"}',
    "created_at": "2025-01-01T00:00:00.000Z",
}

PAYMENT_LINK_DATA = {
    "name": "Pulover azul",
    "product_id": "PVG-AZUL",
    "amount": "10.32",
    "payment_link_url": "https://qvapay.com/payme/abc/10.32",
}

CONTACT_DATA = {
    "uuid": "contact-123",
    "name": "Pedro Perez",
    "username": "pedro",
    "logo": "profiles/pedro.png",
}

DOMAIN_DATA = {"domain": "tienda.qvapay.com", "available": True}
SAVINGS_DATA = {"enabled": True, "balance": "12.50"}
KYC_DATA = {"status": "pending"}
TOPUP_DATA = {"invoice": "inv_123"}
REFERRALS_DATA = {"referrals": 2}
GOLD_DATA = {"active": True}


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/user",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


class TestAsyncUserModule:
    @pytest.mark.anyio
    async def test_submodules(self):
        http = AsyncMock()
        http.get.side_effect = [
            _mock_response(
                [PAYMENT_METHOD_DATA],
                url="https://api.qvapay.com/user/payment-methods",
            ),
            _mock_response(
                [PAYMENT_LINK_DATA],
                url="https://api.qvapay.com/user/payment-links",
            ),
            _mock_response(
                [CONTACT_DATA],
                url="https://api.qvapay.com/user/contact",
            ),
            _mock_response(
                DOMAIN_DATA,
                url="https://api.qvapay.com/domain",
            ),
            _mock_response(
                SAVINGS_DATA,
                url="https://api.qvapay.com/saving",
            ),
            _mock_response(
                SAVINGS_DATA,
                url="https://api.qvapay.com/saving",
            ),
        ]
        http.post.side_effect = [
            _mock_response(
                PAYMENT_METHOD_DATA,
                method="POST",
                url="https://api.qvapay.com/user/payment-methods",
            ),
            _mock_response(
                PAYMENT_LINK_DATA,
                method="POST",
                url="https://api.qvapay.com/user/payment-links",
            ),
            _mock_response(
                CONTACT_DATA,
                method="POST",
                url="https://api.qvapay.com/user/contact",
            ),
            _mock_response(
                DOMAIN_DATA,
                method="POST",
                url="https://api.qvapay.com/domain",
            ),
        ]
        http.delete.return_value = _mock_response(
            {},
            method="DELETE",
            url="https://api.qvapay.com/user/payment-links",
        )
        module = AsyncUserModule(http)

        methods = await module.payment_methods.list()
        created_method = await module.payment_methods.create(type="wallet")
        links = await module.payment_links.list()
        created_link = await module.payment_links.create(name="Test")
        await module.payment_links.delete(12345)
        contacts = await module.contacts.list()
        saved_contact = await module.contacts.save(name="Pedro")
        domain = await module.domains.check("tienda.qvapay.com")
        available = await module.domains.get_available(keyword="tienda")
        savings = await module.savings.status()
        alias_savings = await module.savings_status()

        assert isinstance(methods[0], PaymentMethod)
        assert isinstance(created_method, PaymentMethod)
        assert isinstance(links[0], PaymentLink)
        assert isinstance(created_link, PaymentLink)
        assert isinstance(contacts[0], Contact)
        assert isinstance(saved_contact, Contact)
        assert isinstance(domain, Domain)
        assert isinstance(available, Domain)
        assert savings == SAVINGS_DATA
        assert alias_savings == SAVINGS_DATA
        http.get.assert_any_call("user/payment-methods")
        http.get.assert_any_call("user/payment-links")
        http.get.assert_any_call("user/contact")
        http.get.assert_any_call("domain", params={"name": "tienda.qvapay.com"})
        http.get.assert_any_call("saving")
        http.post.assert_any_call("user/payment-methods", json={"type": "wallet"})
        http.post.assert_any_call("user/payment-links", json={"name": "Test"})
        http.post.assert_any_call("user/contact", json={"name": "Pedro"})
        http.post.assert_any_call("domain", json={"keyword": "tienda"})
        http.delete.assert_called_once_with(
            "user/payment-links",
            json={"id": 12345},
        )

    @pytest.mark.anyio
    async def test_profile_operations(self):
        http = AsyncMock()
        http.get.side_effect = [
            _mock_response(USER_DATA, url="https://api.qvapay.com/user"),
            _mock_response(USER_DATA, url="https://api.qvapay.com/user/extended"),
            _mock_response(KYC_DATA, url="https://api.qvapay.com/user/kyc"),
            _mock_response(REFERRALS_DATA, url="https://api.qvapay.com/user/referrals"),
            _mock_response(GOLD_DATA, url="https://api.qvapay.com/user/gold"),
        ]
        http.put.side_effect = [
            _mock_response(
                USER_DATA, method="PUT", url="https://api.qvapay.com/user/update"
            ),
            _mock_response(
                USER_DATA,
                method="PUT",
                url="https://api.qvapay.com/user/update/email",
            ),
            _mock_response(
                USER_DATA,
                method="PUT",
                url="https://api.qvapay.com/user/update/email",
            ),
            _mock_response(
                USER_DATA,
                method="PUT",
                url="https://api.qvapay.com/user/update/username",
            ),
        ]
        http.post.side_effect = [
            _mock_response(
                USER_DATA, method="POST", url="https://api.qvapay.com/user/avatar"
            ),
            _mock_response(
                USER_DATA, method="POST", url="https://api.qvapay.com/user/avatar"
            ),
            _mock_response(
                KYC_DATA, method="POST", url="https://api.qvapay.com/user/kyc"
            ),
            _mock_response(
                TOPUP_DATA, method="POST", url="https://api.qvapay.com/topup"
            ),
            _mock_response(
                TOPUP_DATA, method="POST", url="https://api.qvapay.com/topup"
            ),
            _mock_response(
                [USER_DATA], method="POST", url="https://api.qvapay.com/user/search"
            ),
            _mock_response(
                GOLD_DATA, method="POST", url="https://api.qvapay.com/user/gold"
            ),
        ]
        module = AsyncUserModule(http)

        me = await module.me()
        me_extended = await module.me_extended()
        updated = await module.update(name="Updated")
        email_first = await module.update_email("new@example.com")
        email_second = await module.update_email("new@example.com", pin="4321")
        username = await module.update_username("new_username")
        avatar = await module.upload_avatar(b"avatar-bytes")
        cover = await module.upload_cover(b"cover-bytes")
        kyc_status = await module.kyc_status()
        kyc_apply = await module.kyc_apply(country="CU")
        topup_default = await module.topup("BTCLN", 10)
        topup_webhook = await module.topup(
            "USDT",
            20,
            webhook_url="https://example.com/hook",
        )
        search = await module.search("sky")
        referrals = await module.referrals()
        gold_status = await module.gold_status()
        gold_purchase = await module.gold_purchase(plan="monthly")

        assert isinstance(me, User)
        assert isinstance(me_extended, User)
        assert isinstance(updated, User)
        assert isinstance(email_first, User)
        assert isinstance(email_second, User)
        assert isinstance(username, User)
        assert isinstance(avatar, User)
        assert isinstance(cover, User)
        assert kyc_status == KYC_DATA
        assert kyc_apply == KYC_DATA
        assert topup_default == TOPUP_DATA
        assert topup_webhook == TOPUP_DATA
        assert isinstance(search[0], User)
        assert referrals == REFERRALS_DATA
        assert gold_status == GOLD_DATA
        assert gold_purchase == GOLD_DATA
        http.put.assert_any_call("user/update", json={"name": "Updated"})
        http.put.assert_any_call(
            "user/update/email",
            json={"email": "new@example.com"},
        )
        http.put.assert_any_call(
            "user/update/email",
            json={"email": "new@example.com", "pin": "4321"},
        )
        http.put.assert_any_call(
            "user/update/username",
            json={"username": "new_username"},
        )
        http.post.assert_any_call(
            "user/avatar",
            data={"type": "avatar"},
            files={"avatar": b"avatar-bytes"},
        )
        http.post.assert_any_call(
            "user/avatar",
            data={"type": "cover"},
            files={"cover": b"cover-bytes"},
        )
        http.post.assert_any_call("user/kyc", json={"country": "CU"})
        http.post.assert_any_call(
            "topup",
            json={"pay_method": "BTCLN", "amount": 10},
        )
        http.post.assert_any_call(
            "topup",
            json={
                "pay_method": "USDT",
                "amount": 20,
                "webhook_url": "https://example.com/hook",
            },
        )
        http.post.assert_any_call("user/search", json={"query": "sky"})
        http.post.assert_any_call("user/gold", json={"plan": "monthly"})


class TestSyncUserModule:
    def test_submodules(self):
        http = MagicMock()
        http.get.side_effect = [
            _mock_response(
                [PAYMENT_METHOD_DATA],
                url="https://api.qvapay.com/user/payment-methods",
            ),
            _mock_response(
                [PAYMENT_LINK_DATA],
                url="https://api.qvapay.com/user/payment-links",
            ),
            _mock_response(
                [CONTACT_DATA],
                url="https://api.qvapay.com/user/contact",
            ),
            _mock_response(
                DOMAIN_DATA,
                url="https://api.qvapay.com/domain",
            ),
            _mock_response(
                SAVINGS_DATA,
                url="https://api.qvapay.com/saving",
            ),
            _mock_response(
                SAVINGS_DATA,
                url="https://api.qvapay.com/saving",
            ),
        ]
        http.post.side_effect = [
            _mock_response(
                PAYMENT_METHOD_DATA,
                method="POST",
                url="https://api.qvapay.com/user/payment-methods",
            ),
            _mock_response(
                PAYMENT_LINK_DATA,
                method="POST",
                url="https://api.qvapay.com/user/payment-links",
            ),
            _mock_response(
                CONTACT_DATA,
                method="POST",
                url="https://api.qvapay.com/user/contact",
            ),
            _mock_response(
                DOMAIN_DATA,
                method="POST",
                url="https://api.qvapay.com/domain",
            ),
        ]
        http.delete.return_value = _mock_response(
            {},
            method="DELETE",
            url="https://api.qvapay.com/user/payment-links",
        )
        module = SyncUserModule(http)

        methods = module.payment_methods.list()
        created_method = module.payment_methods.create(type="wallet")
        links = module.payment_links.list()
        created_link = module.payment_links.create(name="Test")
        module.payment_links.delete(12345)
        contacts = module.contacts.list()
        saved_contact = module.contacts.save(name="Pedro")
        domain = module.domains.check("tienda.qvapay.com")
        available = module.domains.get_available(keyword="tienda")
        savings = module.savings.status()
        alias_savings = module.savings_status()

        assert isinstance(methods[0], PaymentMethod)
        assert isinstance(created_method, PaymentMethod)
        assert isinstance(links[0], PaymentLink)
        assert isinstance(created_link, PaymentLink)
        assert isinstance(contacts[0], Contact)
        assert isinstance(saved_contact, Contact)
        assert isinstance(domain, Domain)
        assert isinstance(available, Domain)
        assert savings == SAVINGS_DATA
        assert alias_savings == SAVINGS_DATA
        http.get.assert_any_call("user/payment-methods")
        http.get.assert_any_call("user/payment-links")
        http.get.assert_any_call("user/contact")
        http.get.assert_any_call("domain", params={"name": "tienda.qvapay.com"})
        http.get.assert_any_call("saving")
        http.post.assert_any_call("user/payment-methods", json={"type": "wallet"})
        http.post.assert_any_call("user/payment-links", json={"name": "Test"})
        http.post.assert_any_call("user/contact", json={"name": "Pedro"})
        http.post.assert_any_call("domain", json={"keyword": "tienda"})
        http.delete.assert_called_once_with(
            "user/payment-links",
            json={"id": 12345},
        )

    def test_profile_operations(self):
        http = MagicMock()
        http.get.side_effect = [
            _mock_response(USER_DATA, url="https://api.qvapay.com/user"),
            _mock_response(USER_DATA, url="https://api.qvapay.com/user/extended"),
            _mock_response(KYC_DATA, url="https://api.qvapay.com/user/kyc"),
            _mock_response(REFERRALS_DATA, url="https://api.qvapay.com/user/referrals"),
            _mock_response(GOLD_DATA, url="https://api.qvapay.com/user/gold"),
        ]
        http.put.side_effect = [
            _mock_response(
                USER_DATA, method="PUT", url="https://api.qvapay.com/user/update"
            ),
            _mock_response(
                USER_DATA,
                method="PUT",
                url="https://api.qvapay.com/user/update/email",
            ),
            _mock_response(
                USER_DATA,
                method="PUT",
                url="https://api.qvapay.com/user/update/email",
            ),
            _mock_response(
                USER_DATA,
                method="PUT",
                url="https://api.qvapay.com/user/update/username",
            ),
        ]
        http.post.side_effect = [
            _mock_response(
                USER_DATA, method="POST", url="https://api.qvapay.com/user/avatar"
            ),
            _mock_response(
                USER_DATA, method="POST", url="https://api.qvapay.com/user/avatar"
            ),
            _mock_response(
                KYC_DATA, method="POST", url="https://api.qvapay.com/user/kyc"
            ),
            _mock_response(
                TOPUP_DATA, method="POST", url="https://api.qvapay.com/topup"
            ),
            _mock_response(
                TOPUP_DATA, method="POST", url="https://api.qvapay.com/topup"
            ),
            _mock_response(
                [USER_DATA], method="POST", url="https://api.qvapay.com/user/search"
            ),
            _mock_response(
                GOLD_DATA, method="POST", url="https://api.qvapay.com/user/gold"
            ),
        ]
        module = SyncUserModule(http)

        me = module.me()
        me_extended = module.me_extended()
        updated = module.update(name="Updated")
        email_first = module.update_email("new@example.com")
        email_second = module.update_email("new@example.com", pin="4321")
        username = module.update_username("new_username")
        avatar = module.upload_avatar(b"avatar-bytes")
        cover = module.upload_cover(b"cover-bytes")
        kyc_status = module.kyc_status()
        kyc_apply = module.kyc_apply(country="CU")
        topup_default = module.topup("BTCLN", 10)
        topup_webhook = module.topup(
            "USDT",
            20,
            webhook_url="https://example.com/hook",
        )
        search = module.search("sky")
        referrals = module.referrals()
        gold_status = module.gold_status()
        gold_purchase = module.gold_purchase(plan="monthly")

        assert isinstance(me, User)
        assert isinstance(me_extended, User)
        assert isinstance(updated, User)
        assert isinstance(email_first, User)
        assert isinstance(email_second, User)
        assert isinstance(username, User)
        assert isinstance(avatar, User)
        assert isinstance(cover, User)
        assert kyc_status == KYC_DATA
        assert kyc_apply == KYC_DATA
        assert topup_default == TOPUP_DATA
        assert topup_webhook == TOPUP_DATA
        assert isinstance(search[0], User)
        assert referrals == REFERRALS_DATA
        assert gold_status == GOLD_DATA
        assert gold_purchase == GOLD_DATA
        http.put.assert_any_call("user/update", json={"name": "Updated"})
        http.put.assert_any_call(
            "user/update/email",
            json={"email": "new@example.com"},
        )
        http.put.assert_any_call(
            "user/update/email",
            json={"email": "new@example.com", "pin": "4321"},
        )
        http.put.assert_any_call(
            "user/update/username",
            json={"username": "new_username"},
        )
        http.post.assert_any_call(
            "user/avatar",
            data={"type": "avatar"},
            files={"avatar": b"avatar-bytes"},
        )
        http.post.assert_any_call(
            "user/avatar",
            data={"type": "cover"},
            files={"cover": b"cover-bytes"},
        )
        http.post.assert_any_call("user/kyc", json={"country": "CU"})
        http.post.assert_any_call(
            "topup",
            json={"pay_method": "BTCLN", "amount": 10},
        )
        http.post.assert_any_call(
            "topup",
            json={
                "pay_method": "USDT",
                "amount": 20,
                "webhook_url": "https://example.com/hook",
            },
        )
        http.post.assert_any_call("user/search", json={"query": "sky"})
        http.post.assert_any_call("user/gold", json={"plan": "monthly"})
