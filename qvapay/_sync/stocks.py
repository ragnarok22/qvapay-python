from typing import Any, List

from ..http import BASE_URL, DEFAULT_TIMEOUT, SyncClient, TimeoutTypes
from ..utils import validate_response


def _client(timeout: TimeoutTypes) -> SyncClient:
    return SyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
    )


def list(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[Any]:
    """Get current stock/exchange data."""
    with _client(timeout) as client:
        response = client.get("stocks/index")
        validate_response(response)
        return response.json()
