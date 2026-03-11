from unittest.mock import AsyncMock, MagicMock

import httpx
import pytest

from qvapay._async.modules.withdraw import WithdrawModule as AsyncWithdrawModule
from qvapay._sync.modules.withdraw import WithdrawModule as SyncWithdrawModule
from qvapay.models.withdrawal import Withdrawal, WithdrawCoin, WithdrawTransaction


def _mock_response(
    json_data,
    status_code: int = 200,
    method: str = "POST",
    url: str = "https://api.qvapay.com/withdraw",
) -> httpx.Response:
    return httpx.Response(
        status_code=status_code,
        json=json_data,
        request=httpx.Request(method, url),
    )


# -- Fixtures --------------------------------------------------------------

# POST create: flat response (BTCLN, BANK_MLC)
FLAT_RESPONSE = {
    "user_id": 54011,
    "transaction_id": 221611,
    "amount": 4,
    "receive": 3.82,
    "payment_method": "BTCLN",
    "details": '[{"Wallet":"bc1qs67kwcf7znpnc06xjh8cnc0zwsechcfxscghun"}]',
    "status": "pending",
    "updated_at": "2022-10-29T00:41:46.000000Z",
    "created_at": "2022-10-29T00:41:46.000000Z",
    "id": 10787,
}

# POST create: wrapped response (USDT, USDCASH)
WRAPPED_RESPONSE = {
    "result": "OK",
    "data": {
        "withdraw_id": "79279",
        "transaction_id": "1776775",
        "receive_amount": 1,
        "receive_amount_coin": 1,
        "fee_to_apply": 1,
        "amount": 2,
        "coin": "USDT",
    },
}

BANK_MLC_RESPONSE = {
    "user_id": 54011,
    "transaction_id": 221612,
    "amount": 30,
    "receive": 28.5,
    "payment_method": "BANK_MLC",
    "details": (
        '[{"Nombre y Apellidos":"Bruno Yosem",'
        '"Nro de tarjeta":"9225 9598 0000 0000",'
        '"Nro de celular":"50000000"}]'
    ),
    "status": "pending",
    "updated_at": "2022-10-29T00:51:47.000000Z",
    "created_at": "2022-10-29T00:51:47.000000Z",
    "id": 10788,
}

USDCASH_RESPONSE = {
    "result": "OK",
    "data": {
        "withdraw_id": "79280",
        "transaction_id": "1776781",
        "receive_amount": 100,
        "receive_amount_coin": 100,
        "fee_to_apply": 0,
        "amount": 100,
        "coin": "USDCASH",
    },
}

# GET list: paginated response with nested objects
LIST_ITEM = {
    "id": 10790,
    "user_id": 54011,
    "transaction_id": 221632,
    "amount": "30.00",
    "receive": "28.50",
    "payment_method": "BANK_MLC",
    "details": '[{"Nombre y Apellidos":"Bruno Yosem"}]',
    "status": "pending",
    "tx_id": None,
    "created_at": "2022-11-28T17:16:38.000000Z",
    "updated_at": "2022-11-28T17:16:38.000000Z",
    "transaction": {
        "uuid": "30b8b187-c9bb-420b-8ca1-f92a3bf2bc29",
        "app_id": 0,
        "amount": "30.00",
        "description": "WITHDRAW",
        "remote_id": "54011",
        "status": "paid",
        "created_at": "2022-11-28T17:15:35.000000Z",
        "updated_at": "2022-11-28T17:15:35.000000Z",
    },
    "coin": {
        "id": 32,
        "coins_categories_id": 2,
        "name": "Banco MLC",
        "logo": "bankmlc",
        "tick": "BANK_MLC",
        "fee_in": "0.00",
        "fee_out": "5.00",
        "min_in": "10.00",
        "min_out": "20.00",
        "price": "1.000000000000000000",
    },
}

LIST_RESPONSE = {
    "current_page": 1,
    "data": [LIST_ITEM],
    "first_page_url": "https://qvapay.test/api/withdraws?page=1",
    "from": 1,
    "last_page": 1,
    "last_page_url": "https://qvapay.test/api/withdraws?page=1",
    "next_page_url": None,
    "path": "https://qvapay.test/api/withdraws",
    "per_page": 10,
    "prev_page_url": None,
    "to": 1,
    "total": 1,
}


# -- Model tests ----------------------------------------------------------


class TestWithdrawalModel:
    def test_from_json_flat_response(self):
        w = Withdrawal.from_json(FLAT_RESPONSE)
        assert w.amount == 4.0
        assert w.transaction_id == "221611"
        assert w.status == "pending"
        assert w.payment_method == "BTCLN"
        assert w.receive == 3.82
        assert w.created_at == "2022-10-29T00:41:46.000000Z"
        assert w.transaction is None
        assert w.coin_detail is None
        assert w.coin is None

    def test_from_json_wrapped_response(self):
        w = Withdrawal.from_json(WRAPPED_RESPONSE)
        assert w.amount == 2.0
        assert w.transaction_id == "1776775"
        assert w.withdraw_id == "79279"
        assert w.coin == "USDT"
        assert w.fee_to_apply == 1
        assert w.receive_amount == 1
        assert w.receive_amount_coin == 1

    def test_from_json_bank_mlc(self):
        w = Withdrawal.from_json(BANK_MLC_RESPONSE)
        assert w.amount == 30.0
        assert w.transaction_id == "221612"
        assert w.payment_method == "BANK_MLC"
        assert w.receive == 28.5

    def test_from_json_usdcash(self):
        w = Withdrawal.from_json(USDCASH_RESPONSE)
        assert w.amount == 100.0
        assert w.transaction_id == "1776781"
        assert w.coin == "USDCASH"
        assert w.fee_to_apply == 0

    def test_from_json_list_item_with_nested_objects(self):
        w = Withdrawal.from_json(LIST_ITEM)
        assert w.amount == 30.0
        assert w.transaction_id == "221632"
        assert w.payment_method == "BANK_MLC"
        assert w.status == "pending"
        assert w.tx_id is None
        # nested transaction
        assert isinstance(w.transaction, WithdrawTransaction)
        assert w.transaction.uuid == "30b8b187-c9bb-420b-8ca1-f92a3bf2bc29"
        assert w.transaction.description == "WITHDRAW"
        assert w.transaction.status == "paid"
        # nested coin → coin_detail
        assert isinstance(w.coin_detail, WithdrawCoin)
        assert w.coin_detail.tick == "BANK_MLC"
        assert w.coin_detail.name == "Banco MLC"
        assert w.coin_detail.fee_out == "5.00"
        # string coin should be None when coin is an object
        assert w.coin is None


# -- Async module tests ----------------------------------------------------


class TestAsyncWithdrawCreate:
    @pytest.mark.anyio
    async def test_create_crypto(self):
        http = AsyncMock()
        http.post.return_value = _mock_response(WRAPPED_RESPONSE)
        module = AsyncWithdrawModule(http)

        result = await module.create(
            "USDT",
            2,
            {"Wallet": "TEvQ7WSPCbJCKVC7qLo29L6zGJb2VQBRVy"},
            pin=1234,
            note="test withdrawal",
        )

        http.post.assert_called_once_with(
            "withdraw",
            json={
                "pay_method": "USDT",
                "amount": 2,
                "details": {"Wallet": "TEvQ7WSPCbJCKVC7qLo29L6zGJb2VQBRVy"},
                "pin": 1234,
                "note": "test withdrawal",
            },
        )
        assert isinstance(result, Withdrawal)
        assert result.amount == 2.0
        assert result.coin == "USDT"

    @pytest.mark.anyio
    async def test_create_bank_mlc(self):
        http = AsyncMock()
        http.post.return_value = _mock_response(BANK_MLC_RESPONSE)
        module = AsyncWithdrawModule(http)

        details = {
            "Nombre y Apellidos": "Bruno Yosem",
            "Nro de tarjeta": "9225 9598 0000 0000",
            "Nro de celular": "50000000",
        }
        result = await module.create("BANK_MLC", 30, details)

        http.post.assert_called_once_with(
            "withdraw",
            json={
                "pay_method": "BANK_MLC",
                "amount": 30,
                "details": details,
            },
        )
        assert result.amount == 30.0
        assert result.payment_method == "BANK_MLC"

    @pytest.mark.anyio
    async def test_create_without_pin_and_note(self):
        http = AsyncMock()
        http.post.return_value = _mock_response(FLAT_RESPONSE)
        module = AsyncWithdrawModule(http)

        await module.create(
            "BTCLN",
            4,
            {"Wallet": "bc1qs67kwcf7znpnc06xjh8cnc0zwsechcfxscghun"},
        )

        payload = http.post.call_args[1]["json"]
        assert "pin" not in payload
        assert "note" not in payload

    @pytest.mark.anyio
    async def test_create_usdcash(self):
        http = AsyncMock()
        http.post.return_value = _mock_response(USDCASH_RESPONSE)
        module = AsyncWithdrawModule(http)

        details = {
            "Nombre y Apellidos": "Pepe Conejito",
            "Carnet de Identidad": "121212121212",
            "Nro de Celular": "51212121212",
            "Dirección": "Calle, Numero, Entrecalles",
            "Municipio": "Arroyo Naranjo",
            "Provincia": "La Habana",
        }
        result = await module.create("USDCASH", 100, details, pin=1234, note="efectivo")

        assert result.amount == 100.0
        assert result.coin == "USDCASH"
        assert result.fee_to_apply == 0


class TestAsyncWithdrawList:
    @pytest.mark.anyio
    async def test_list(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(
            LIST_RESPONSE, method="GET", url="https://api.qvapay.com/withdraws"
        )
        module = AsyncWithdrawModule(http)

        results = await module.list()

        http.get.assert_called_once_with("withdraws")
        assert len(results) == 1
        assert isinstance(results[0], Withdrawal)
        assert results[0].amount == 30.0
        assert isinstance(results[0].transaction, WithdrawTransaction)
        assert isinstance(results[0].coin_detail, WithdrawCoin)


class TestAsyncWithdrawGet:
    @pytest.mark.anyio
    async def test_get(self):
        http = AsyncMock()
        http.get.return_value = _mock_response(
            LIST_ITEM, method="GET", url="https://api.qvapay.com/withdraw/10790"
        )
        module = AsyncWithdrawModule(http)

        result = await module.get(10790)

        http.get.assert_called_once_with("withdraw/10790")
        assert isinstance(result, Withdrawal)
        assert result.id == 10790
        assert result.amount == 30.0
        assert result.payment_method == "BANK_MLC"
        assert isinstance(result.transaction, WithdrawTransaction)
        assert result.transaction.uuid == "30b8b187-c9bb-420b-8ca1-f92a3bf2bc29"
        assert isinstance(result.coin_detail, WithdrawCoin)
        assert result.coin_detail.tick == "BANK_MLC"


# -- Sync module tests -----------------------------------------------------


class TestSyncWithdrawCreate:
    def test_create_crypto(self):
        http = MagicMock()
        http.post.return_value = _mock_response(WRAPPED_RESPONSE)
        module = SyncWithdrawModule(http)

        result = module.create(
            "USDT",
            2,
            {"Wallet": "TEvQ7WSPCbJCKVC7qLo29L6zGJb2VQBRVy"},
            pin=1234,
            note="test withdrawal",
        )

        http.post.assert_called_once_with(
            "withdraw",
            json={
                "pay_method": "USDT",
                "amount": 2,
                "details": {"Wallet": "TEvQ7WSPCbJCKVC7qLo29L6zGJb2VQBRVy"},
                "pin": 1234,
                "note": "test withdrawal",
            },
        )
        assert isinstance(result, Withdrawal)
        assert result.amount == 2.0
        assert result.coin == "USDT"

    def test_create_bank_mlc(self):
        http = MagicMock()
        http.post.return_value = _mock_response(BANK_MLC_RESPONSE)
        module = SyncWithdrawModule(http)

        details = {
            "Nombre y Apellidos": "Bruno Yosem",
            "Nro de tarjeta": "9225 9598 0000 0000",
            "Nro de celular": "50000000",
        }
        result = module.create("BANK_MLC", 30, details)

        assert result.amount == 30.0
        assert result.payment_method == "BANK_MLC"

    def test_create_without_pin_and_note(self):
        http = MagicMock()
        http.post.return_value = _mock_response(FLAT_RESPONSE)
        module = SyncWithdrawModule(http)

        module.create(
            "BTCLN",
            4,
            {"Wallet": "bc1qs67kwcf7znpnc06xjh8cnc0zwsechcfxscghun"},
        )

        payload = http.post.call_args[1]["json"]
        assert "pin" not in payload
        assert "note" not in payload

    def test_create_usdcash(self):
        http = MagicMock()
        http.post.return_value = _mock_response(USDCASH_RESPONSE)
        module = SyncWithdrawModule(http)

        details = {
            "Nombre y Apellidos": "Pepe Conejito",
            "Carnet de Identidad": "121212121212",
            "Nro de Celular": "51212121212",
            "Dirección": "Calle, Numero, Entrecalles",
            "Municipio": "Arroyo Naranjo",
            "Provincia": "La Habana",
        }
        result = module.create("USDCASH", 100, details, pin=1234, note="efectivo")

        assert result.amount == 100.0
        assert result.coin == "USDCASH"
        assert result.fee_to_apply == 0


class TestSyncWithdrawList:
    def test_list(self):
        http = MagicMock()
        http.get.return_value = _mock_response(
            LIST_RESPONSE, method="GET", url="https://api.qvapay.com/withdraws"
        )
        module = SyncWithdrawModule(http)

        results = module.list()

        http.get.assert_called_once_with("withdraws")
        assert len(results) == 1
        assert isinstance(results[0], Withdrawal)
        assert results[0].amount == 30.0
        assert isinstance(results[0].transaction, WithdrawTransaction)
        assert isinstance(results[0].coin_detail, WithdrawCoin)


class TestSyncWithdrawGet:
    def test_get(self):
        http = MagicMock()
        http.get.return_value = _mock_response(
            LIST_ITEM, method="GET", url="https://api.qvapay.com/withdraw/10790"
        )
        module = SyncWithdrawModule(http)

        result = module.get(10790)

        http.get.assert_called_once_with("withdraw/10790")
        assert isinstance(result, Withdrawal)
        assert result.id == 10790
        assert result.amount == 30.0
        assert result.payment_method == "BANK_MLC"
        assert isinstance(result.transaction, WithdrawTransaction)
        assert isinstance(result.coin_detail, WithdrawCoin)
