from typing import List

from ..http import BASE_URL, DEFAULT_TIMEOUT, SyncClient, TimeoutTypes
from ..models.coin import CoinCategory
from ..utils import validate_response


def _client(timeout: TimeoutTypes) -> SyncClient:
    return SyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
    )


def list(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[CoinCategory]:
    """Get current stock/exchange data."""
    with _client(timeout) as client:
        response = client.get("coins")
        validate_response(response)
        return [CoinCategory.from_json(item) for item in response.json()]
