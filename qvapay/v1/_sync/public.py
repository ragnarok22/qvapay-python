from typing import List

from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..http_clients import SyncClient
from ..models.coin import CoinCategory
from ..utils import validate_response

BASE_URL = "https://qvapay.com/api"


def _client(timeout: TimeoutTypes) -> SyncClient:
    return SyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
    )


def get_coins(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> List[CoinCategory]:
    """Get available coins grouped by category."""
    with _client(timeout) as client:
        response = client.get("coins")
        validate_response(response)
        return [
            CoinCategory.from_json(item)
            for item in response.json()
        ]


def get_p2p_pairs_average(
    coin: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> float:
    """Get P2P completed pairs average for a given coin."""
    with _client(timeout) as client:
        response = client.get(
            "p2p/completed_pairs_average",
            params={"coin": coin.upper()},
        )
        validate_response(response)
        return float(response.text)
