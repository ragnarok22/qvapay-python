from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.transactions import (
    TransactionsModule as AsyncTransactionsModule,
)
from qvapay._sync.modules.transactions import (
    TransactionsModule as SyncTransactionsModule,
)
from qvapay.models.transaction import (
    Service,
    ServiceBuy,
    Transaction,
    TransactionApp,
    TransactionDetail,
    TransactionUser,
    Wallet,
)

PAID_BY_DATA = {
    "uuid": "user123abc",
    "username": "johndoe",
    "name": "John",
    "lastname": "Doe",
    "bio": "",
    "logo": "",
    "kyc": 0,
}

OWNER_DATA = {
    "uuid": "owner123abc",
    "username": "janesmith",
    "name": "Jane",
    "lastname": "Smith",
    "bio": "Developer",
    "logo": "profiles/jane.jpg",
    "kyc": 1,
}

APP_DATA = {
    "logo": "apps/qvapay.jpg",
    "url": "https://qvapay.com",
    "name": "QvaPay",
}

WALLET_DATA = {
    "transaction_id": 3567,
    "invoice_id": "",
    "wallet_type": "BUSDBSC",
    "wallet": "0x1234567890abcdef",
    "value": "10.09",
    "received": "10.09",
    "txid": "0xabc123def456",
    "status": "paid",
    "created_at": "2021-08-28T21:13:41.000000Z",
    "updated_at": "2021-08-28T21:41:40.000000Z",
}

SERVICE_DATA = {
    "uuid": "service123abc",
    "name": "Tarjeta App Store",
    "lead": "$ 10",
    "price": "10.50",
    "logo": "services/appstore.png",
    "sublogo": "services/appstore_sub.png",
    "desc": "Apple products and services",
}

SERVICEBUY_DATA = {
    "service_id": 14,
    "service_data": '{"phone":"5355149081","confirmationCode":3541}',
    "status": "paid",
    "amount": "20.80",
    "transaction_id": 3541,
    "created_at": "2021-08-05T00:32:56.000000Z",
    "updated_at": "2021-08-05T00:32:56.000000Z",
    "service": SERVICE_DATA,
}

TX_SIMPLE = {
    "uuid": "tx123abc",
    "app_id": 0,
    "amount": "-1",
    "description": "Pollo por pescado",
    "remote_id": "QVAPAY_APP",
    "status": "paid",
    "created_at": "2021-09-06T03:00:47.000000Z",
    "updated_at": "2021-09-06T03:01:05.000000Z",
    "logo": "apps/qvapay.jpg",
    "app": APP_DATA,
    "paid_by": PAID_BY_DATA,
    "app_owner": APP_DATA,
    "owner": OWNER_DATA,
    "wallet": None,
    "servicebuy": None,
}

TX_WITH_WALLET = {
    "uuid": "tx456def",
    "app_id": 0,
    "amount": "10.00",
    "description": "AUTO_RECARGA",
    "remote_id": "2",
    "status": "paid",
    "created_at": "2021-08-28T21:13:38.000000Z",
    "updated_at": "2021-08-28T21:41:41.000000Z",
    "logo": "apps/qvapay.jpg",
    "app": APP_DATA,
    "paid_by": {"username": "QvaPay", "name": "QvaPay", "logo": "apps/qvapay.jpg"},
    "app_owner": APP_DATA,
    "owner": PAID_BY_DATA,
    "wallet": WALLET_DATA,
    "servicebuy": None,
}

TX_WITH_SERVICEBUY = {
    "uuid": "tx789ghi",
    "app_id": 0,
    "amount": "-20.8",
    "description": "Mobile TOP_UP",
    "remote_id": "35415355149081",
    "status": "paid",
    "created_at": "2021-08-05T00:32:45.000000Z",
    "updated_at": "2021-08-05T00:32:56.000000Z",
    "logo": "services/appstore.png",
    "app": APP_DATA,
    "paid_by": PAID_BY_DATA,
    "app_owner": APP_DATA,
    "owner": OWNER_DATA,
    "wallet": None,
    "servicebuy": SERVICEBUY_DATA,
}

TX_DETAIL = {
    **TX_SIMPLE,
    "paid_by_user_id": "user123abc",
}

LIST_RESPONSE = [TX_SIMPLE, TX_WITH_WALLET, TX_WITH_SERVICEBUY]


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "GET",
    url: str = "https://api.qvapay.com/transactions",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


# -- Model tests -------------------------------------------------------------


class TestTransactionApp:
    def test_from_json(self):
        app = TransactionApp.from_json(APP_DATA)
        assert app.name == "QvaPay"
        assert app.logo == "apps/qvapay.jpg"
        assert app.url == "https://qvapay.com"


class TestTransactionUser:
    def test_from_json_full(self):
        user = TransactionUser.from_json(OWNER_DATA)
        assert user.uuid == "owner123abc"
        assert user.username == "janesmith"
        assert user.name == "Jane"
        assert user.lastname == "Smith"
        assert user.bio == "Developer"
        assert user.kyc == 1

    def test_from_json_minimal(self):
        minimal = {"username": "QvaPay", "name": "QvaPay", "logo": "apps/qvapay.jpg"}
        user = TransactionUser.from_json(minimal)
        assert user.name == "QvaPay"
        assert user.uuid is None
        assert user.lastname is None


class TestWallet:
    def test_from_json(self):
        wallet = Wallet.from_json(WALLET_DATA)
        assert wallet.transaction_id == 3567
        assert wallet.wallet_type == "BUSDBSC"
        assert wallet.wallet == "0x1234567890abcdef"
        assert wallet.value == "10.09"
        assert wallet.received == "10.09"
        assert wallet.txid == "0xabc123def456"
        assert wallet.status == "paid"


class TestService:
    def test_from_json(self):
        service = Service.from_json(SERVICE_DATA)
        assert service.uuid == "service123abc"
        assert service.name == "Tarjeta App Store"
        assert service.price == "10.50"
        assert service.desc == "Apple products and services"


class TestServiceBuy:
    def test_from_json(self):
        sb = ServiceBuy.from_json(SERVICEBUY_DATA)
        assert sb.service_id == 14
        assert sb.status == "paid"
        assert sb.amount == "20.80"
        assert sb.transaction_id == 3541
        assert isinstance(sb.service, Service)
        assert sb.service.name == "Tarjeta App Store"

    def test_from_json_without_service(self):
        data = {**SERVICEBUY_DATA, "service": None}
        sb = ServiceBuy.from_json(data)
        assert sb.service is None


class TestTransaction:
    def test_from_json_simple(self):
        tx = Transaction.from_json(TX_SIMPLE)
        assert tx.uuid == "tx123abc"
        assert tx.amount == -1.0
        assert tx.description == "Pollo por pescado"
        assert tx.remote_id == "QVAPAY_APP"
        assert tx.status == "paid"
        assert isinstance(tx.app, TransactionApp)
        assert isinstance(tx.paid_by, TransactionUser)
        assert isinstance(tx.owner, TransactionUser)
        assert tx.wallet is None
        assert tx.servicebuy is None

    def test_from_json_with_wallet(self):
        tx = Transaction.from_json(TX_WITH_WALLET)
        assert tx.uuid == "tx456def"
        assert tx.amount == 10.0
        assert isinstance(tx.wallet, Wallet)
        assert tx.wallet.wallet_type == "BUSDBSC"
        assert tx.servicebuy is None

    def test_from_json_with_servicebuy(self):
        tx = Transaction.from_json(TX_WITH_SERVICEBUY)
        assert tx.uuid == "tx789ghi"
        assert tx.amount == -20.8
        assert isinstance(tx.servicebuy, ServiceBuy)
        assert tx.servicebuy.service_id == 14
        assert isinstance(tx.servicebuy.service, Service)
        assert tx.wallet is None

    def test_amount_coerced_to_float(self):
        tx = Transaction.from_json(TX_SIMPLE)
        assert isinstance(tx.amount, float)
        assert tx.amount == -1.0

    def test_from_json_minimal(self):
        minimal = {
            "uuid": "abc",
            "amount": "5.00",
            "description": "test",
            "remote_id": "r1",
            "status": "pending",
            "created_at": "2021-01-01T00:00:00.000000Z",
            "updated_at": "2021-01-01T00:00:00.000000Z",
        }
        tx = Transaction.from_json(minimal)
        assert tx.uuid == "abc"
        assert tx.amount == 5.0
        assert tx.app is None
        assert tx.paid_by is None
        assert tx.owner is None


# -- Async module tests ------------------------------------------------------


class TestAsyncTransactionsList:
    @pytest.mark.anyio
    async def test_list_no_filters(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = AsyncTransactionsModule(http)

        txs = await module.list()

        http.get.assert_called_once_with("transactions", params={})
        assert len(txs) == 3
        assert all(isinstance(t, Transaction) for t in txs)
        assert txs[0].uuid == "tx123abc"
        assert txs[1].uuid == "tx456def"
        assert txs[2].uuid == "tx789ghi"

    @pytest.mark.anyio
    async def test_list_with_status_filter(self):
        http = AsyncMock()
        http.get.return_value = _mock_response([TX_SIMPLE])
        module = AsyncTransactionsModule(http)

        txs = await module.list(status="paid")

        http.get.assert_called_once_with("transactions", params={"status": "paid"})
        assert len(txs) == 1

    @pytest.mark.anyio
    async def test_list_with_date_filters(self):
        http = AsyncMock()
        http.get.return_value = _mock_response([TX_SIMPLE])
        module = AsyncTransactionsModule(http)

        txs = await module.list(
            start="2021-10-17 13:05:30",
            end="2021-10-17 13:10:10",
        )

        http.get.assert_called_once_with(
            "transactions",
            params={
                "start": "2021-10-17 13:05:30",
                "end": "2021-10-17 13:10:10",
            },
        )
        assert len(txs) == 1

    @pytest.mark.anyio
    async def test_list_with_all_filters(self):
        http = AsyncMock()
        http.get.return_value = _mock_response([TX_SIMPLE])
        module = AsyncTransactionsModule(http)

        await module.list(
            start="2021-10-17 13:05:30",
            end="2021-10-17 13:10:10",
            status="paid",
            remote_id="QVAPAY_APP",
            description="TShirt",
        )

        call_params = http.get.call_args[1]["params"]
        assert call_params["start"] == "2021-10-17 13:05:30"
        assert call_params["end"] == "2021-10-17 13:10:10"
        assert call_params["status"] == "paid"
        assert call_params["remote_id"] == "QVAPAY_APP"
        assert call_params["description"] == "TShirt"

    @pytest.mark.anyio
    async def test_list_omits_none_filters(self):
        http = AsyncMock()
        http.get.return_value = _mock_response([])
        module = AsyncTransactionsModule(http)

        await module.list(status="pending", remote_id=None)

        call_params = http.get.call_args[1]["params"]
        assert "status" in call_params
        assert "remote_id" not in call_params

    @pytest.mark.anyio
    async def test_list_returns_wallet_and_servicebuy(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = AsyncTransactionsModule(http)

        txs = await module.list()

        assert txs[1].wallet is not None
        assert txs[1].wallet.wallet_type == "BUSDBSC"
        assert txs[2].servicebuy is not None
        assert txs[2].servicebuy.service_id == 14


# -- Sync module tests -------------------------------------------------------


class TestSyncTransactionsList:
    def test_list_no_filters(self):
        http = MagicMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = SyncTransactionsModule(http)

        txs = module.list()

        http.get.assert_called_once_with("transactions", params={})
        assert len(txs) == 3
        assert all(isinstance(t, Transaction) for t in txs)
        assert txs[0].uuid == "tx123abc"

    def test_list_with_status_filter(self):
        http = MagicMock()
        http.get.return_value = _mock_response([TX_SIMPLE])
        module = SyncTransactionsModule(http)

        txs = module.list(status="paid")

        http.get.assert_called_once_with("transactions", params={"status": "paid"})
        assert len(txs) == 1

    def test_list_with_all_filters(self):
        http = MagicMock()
        http.get.return_value = _mock_response([TX_SIMPLE])
        module = SyncTransactionsModule(http)

        module.list(
            start="2021-10-17 13:05:30",
            end="2021-10-17 13:10:10",
            status="paid",
            remote_id="QVAPAY_APP",
            description="TShirt",
        )

        call_params = http.get.call_args[1]["params"]
        assert call_params["start"] == "2021-10-17 13:05:30"
        assert call_params["end"] == "2021-10-17 13:10:10"
        assert call_params["status"] == "paid"
        assert call_params["remote_id"] == "QVAPAY_APP"
        assert call_params["description"] == "TShirt"

    def test_list_returns_nested_objects(self):
        http = MagicMock()
        http.get.return_value = _mock_response(LIST_RESPONSE)
        module = SyncTransactionsModule(http)

        txs = module.list()

        assert isinstance(txs[0].app, TransactionApp)
        assert isinstance(txs[0].paid_by, TransactionUser)
        assert txs[1].wallet is not None
        assert txs[2].servicebuy is not None


# -- TransactionDetail model tests ------------------------------------------


class TestTransactionDetail:
    def test_from_json(self):
        td = TransactionDetail.from_json(TX_DETAIL)
        assert isinstance(td, TransactionDetail)
        assert td.uuid == "tx123abc"
        assert td.paid_by_user_id == "user123abc"
        assert td.amount == -1.0
        assert isinstance(td.app, TransactionApp)
        assert isinstance(td.paid_by, TransactionUser)

    def test_from_json_without_paid_by_user_id(self):
        td = TransactionDetail.from_json(TX_SIMPLE)
        assert isinstance(td, TransactionDetail)
        assert td.paid_by_user_id is None


# -- Async get tests ---------------------------------------------------------


class TestAsyncTransactionsGet:
    @pytest.mark.anyio
    async def test_get(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(TX_DETAIL)
        module = AsyncTransactionsModule(http)

        tx = await module.get("tx123abc")

        http.get.assert_called_once_with("transaction/tx123abc")
        assert isinstance(tx, TransactionDetail)
        assert tx.uuid == "tx123abc"
        assert tx.paid_by_user_id == "user123abc"


# -- Sync get tests ----------------------------------------------------------


class TestSyncTransactionsGet:
    def test_get(self):
        http = MagicMock()
        http.get.return_value = _mock_response(TX_DETAIL)
        module = SyncTransactionsModule(http)

        tx = module.get("tx123abc")

        http.get.assert_called_once_with("transaction/tx123abc")
        assert isinstance(tx, TransactionDetail)
        assert tx.uuid == "tx123abc"
        assert tx.paid_by_user_id == "user123abc"
