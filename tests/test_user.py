from unittest.mock import AsyncMock, MagicMock

import pytest

from qvapay._async.modules.user import (
    UserPaymentLinksSubModule as AsyncUserPaymentLinksSubModule,
)
from qvapay._sync.modules.user import (
    UserPaymentLinksSubModule as SyncUserPaymentLinksSubModule,
)


class TestAsyncUserPaymentLinksSubModule:
    @pytest.mark.anyio
    async def test_delete_sends_documented_delete_body(self):
        http = AsyncMock()
        http.delete.return_value.is_success = True
        http.delete.return_value.headers = {"content-type": "application/json"}
        module = AsyncUserPaymentLinksSubModule(http)

        await module.delete(12345)

        http.delete.assert_called_once_with(
            "user/payment-links",
            json={"id": 12345},
        )


class TestSyncUserPaymentLinksSubModule:
    def test_delete_sends_documented_delete_body(self):
        http = MagicMock()
        http.delete.return_value.is_success = True
        http.delete.return_value.headers = {"content-type": "application/json"}
        module = SyncUserPaymentLinksSubModule(http)

        module.delete(12345)

        http.delete.assert_called_once_with(
            "user/payment-links",
            json={"id": 12345},
        )
