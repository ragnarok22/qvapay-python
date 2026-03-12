from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from qvapay._async.merchant import AsyncQvaPayMerchant
from qvapay._sync.merchant import SyncQvaPayMerchant
from qvapay.http import V2_BASE_URL
from qvapay.models.invoice import Invoice
from qvapay.models.transaction import PaginatedTransactions

APP_UUID = "12345678-1234-1234-1234-1234567890ab"
APP_SECRET = "secret-key"
AUTH_PAYLOAD = {"app_id": APP_UUID, "app_secret": APP_SECRET}

INVOICE_DATA = {
    "app_id": "1",
    "amount": "10.00",
    "description": "QvaPay shirt",
    "remote_id": "remote-123",
    "signed": "1",
    "transation_uuid": "tx-123",
    "url": "https://qvapay.com/pay/tx-123",
    "signedUrl": "https://qvapay.com/pay/tx-123?signed=1",
}

TRANSACTION_DATA = {
    "uuid": "2f76f05e-2cda-4042-9e97-3777745d740e",
    "app_id": 0,
    "amount": "-1",
    "description": "Pollo por pescado",
    "remote_id": "QVAPAY_APP",
    "status": "paid",
    "created_at": "2021-09-06T03:00:47.000000Z",
    "updated_at": "2021-09-06T03:01:05.000000Z",
}

TRANSACTIONS_DATA = {"current_page": 1, "data": [TRANSACTION_DATA], "total": 1}
STATUS_DATA = {"status": "paid"}
AUTHORIZATION_DATA = {"url": "https://qvapay.com/authorize"}
CHARGE_DATA = {"message": "charged"}


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "POST",
    url: str = "https://api.qvapay.com/v2/info",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


class TestAsyncMerchantExtra:
    @pytest.mark.anyio
    async def test_init_context_and_close(self):
        http = MagicMock()
        http.aclose = AsyncMock()

        with patch(
            "qvapay._async.merchant.AsyncClient",
            return_value=http,
        ) as client_cls:
            merchant = AsyncQvaPayMerchant(APP_UUID, APP_SECRET)

        kwargs = client_cls.call_args.kwargs
        assert kwargs["base_url"] == V2_BASE_URL
        assert kwargs["follow_redirects"] is True
        assert await merchant.__aenter__() is merchant
        await merchant.__aexit__(None, None, None)
        http.aclose.assert_awaited_once()

    @pytest.mark.anyio
    async def test_invoice_and_transactions_operations(self):
        merchant = AsyncQvaPayMerchant(APP_UUID, APP_SECRET)
        merchant._http = AsyncMock()
        merchant._http.post.side_effect = [
            _mock_response(
                INVOICE_DATA, url="https://api.qvapay.com/v2/create_invoice"
            ),
            _mock_response(
                INVOICE_DATA, url="https://api.qvapay.com/v2/modify_invoice"
            ),
            _mock_response(
                TRANSACTIONS_DATA, url="https://api.qvapay.com/v2/transactions"
            ),
            _mock_response(
                STATUS_DATA, url="https://api.qvapay.com/v2/transactions/tx-123"
            ),
            _mock_response(
                AUTHORIZATION_DATA,
                url="https://api.qvapay.com/v2/authorize_payments",
            ),
            _mock_response(CHARGE_DATA, url="https://api.qvapay.com/v2/charge"),
        ]

        created = await merchant.create_invoice(10, "QvaPay shirt", "remote-123", True)
        modified = await merchant.modify_invoice("tx-123", amount=15)
        transactions = await merchant.get_transactions()
        status = await merchant.get_transaction_status("tx-123")
        authorization = await merchant.get_payments_authorization(token="abc")
        charge = await merchant.charge_user(token="abc", amount=10)

        assert isinstance(created, Invoice)
        assert isinstance(modified, Invoice)
        assert isinstance(transactions, PaginatedTransactions)
        assert transactions.total == 1
        assert status == STATUS_DATA
        assert authorization == AUTHORIZATION_DATA
        assert charge == CHARGE_DATA
        merchant._http.post.assert_any_call(
            "create_invoice",
            json={
                **AUTH_PAYLOAD,
                "amount": 10,
                "description": "QvaPay shirt",
                "remote_id": "remote-123",
                "signed": 1,
            },
        )
        merchant._http.post.assert_any_call(
            "modify_invoice",
            json={**AUTH_PAYLOAD, "uuid": "tx-123", "amount": 15},
        )
        merchant._http.post.assert_any_call("transactions", json=AUTH_PAYLOAD)
        merchant._http.post.assert_any_call(
            "transactions/tx-123",
            json={**AUTH_PAYLOAD, "uuid": "tx-123"},
        )
        merchant._http.post.assert_any_call(
            "authorize_payments",
            json={**AUTH_PAYLOAD, "token": "abc"},
        )
        merchant._http.post.assert_any_call(
            "charge",
            json={**AUTH_PAYLOAD, "token": "abc", "amount": 10},
        )


class TestSyncMerchantExtra:
    def test_init_context_and_close(self):
        http = MagicMock()

        with patch("qvapay._sync.merchant.SyncClient", return_value=http) as client_cls:
            merchant = SyncQvaPayMerchant(APP_UUID, APP_SECRET)

        kwargs = client_cls.call_args.kwargs
        assert kwargs["base_url"] == V2_BASE_URL
        assert kwargs["follow_redirects"] is True
        assert merchant.__enter__() is merchant
        merchant.__exit__(None, None, None)
        http.aclose.assert_called_once_with()

    def test_invoice_and_transactions_operations(self):
        merchant = SyncQvaPayMerchant(APP_UUID, APP_SECRET)
        merchant._http = MagicMock()
        merchant._http.post.side_effect = [
            _mock_response(
                INVOICE_DATA, url="https://api.qvapay.com/v2/create_invoice"
            ),
            _mock_response(
                INVOICE_DATA, url="https://api.qvapay.com/v2/modify_invoice"
            ),
            _mock_response(
                TRANSACTIONS_DATA, url="https://api.qvapay.com/v2/transactions"
            ),
            _mock_response(
                STATUS_DATA, url="https://api.qvapay.com/v2/transactions/tx-123"
            ),
            _mock_response(
                AUTHORIZATION_DATA,
                url="https://api.qvapay.com/v2/authorize_payments",
            ),
            _mock_response(CHARGE_DATA, url="https://api.qvapay.com/v2/charge"),
        ]

        created = merchant.create_invoice(10, "QvaPay shirt", "remote-123", True)
        modified = merchant.modify_invoice("tx-123", amount=15)
        transactions = merchant.get_transactions()
        status = merchant.get_transaction_status("tx-123")
        authorization = merchant.get_payments_authorization(token="abc")
        charge = merchant.charge_user(token="abc", amount=10)

        assert isinstance(created, Invoice)
        assert isinstance(modified, Invoice)
        assert isinstance(transactions, PaginatedTransactions)
        assert transactions.total == 1
        assert status == STATUS_DATA
        assert authorization == AUTHORIZATION_DATA
        assert charge == CHARGE_DATA
        merchant._http.post.assert_any_call(
            "create_invoice",
            json={
                **AUTH_PAYLOAD,
                "amount": 10,
                "description": "QvaPay shirt",
                "remote_id": "remote-123",
                "signed": 1,
            },
        )
        merchant._http.post.assert_any_call(
            "modify_invoice",
            json={**AUTH_PAYLOAD, "uuid": "tx-123", "amount": 15},
        )
        merchant._http.post.assert_any_call("transactions", json=AUTH_PAYLOAD)
        merchant._http.post.assert_any_call(
            "transactions/tx-123",
            json={**AUTH_PAYLOAD, "uuid": "tx-123"},
        )
        merchant._http.post.assert_any_call(
            "authorize_payments",
            json={**AUTH_PAYLOAD, "token": "abc"},
        )
        merchant._http.post.assert_any_call(
            "charge",
            json={**AUTH_PAYLOAD, "token": "abc", "amount": 10},
        )
