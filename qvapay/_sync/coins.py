from typing import List

from ..http import BASE_URL, DEFAULT_TIMEOUT, SyncClient, TimeoutTypes
from ..models.coin import Coin, CoinCategory
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
    """Get available coins grouped by category."""
    with _client(timeout) as client:
        response = client.get("coins")
        validate_response(response)
        return [CoinCategory.from_json(item) for item in response.json()]


def list_v2(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[CoinCategory]:
    """Get available coins (v2 format)."""
    with _client(timeout) as client:
        response = client.get("v2/coins")
        validate_response(response)
        return [CoinCategory.from_json(item) for item in response.json()]


def get(
    coin_id: int,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> Coin:
    """Get a specific coin by ID."""
    with _client(timeout) as client:
        response = client.get(f"coins/{coin_id}")
        validate_response(response)
        return Coin.from_json(response.json())


def history(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> list:
    """Get coins price history."""
    with _client(timeout) as client:
        response = client.get("coins/history")
        validate_response(response)
        return response.json()
