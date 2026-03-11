from typing import List

from httpx._config import DEFAULT_TIMEOUT_CONFIG
from httpx._types import TimeoutTypes

from ..http_clients import SyncClient
from ..models.coin import Coin
from ..models.rate import Rate
from ..utils import validate_response

BASE_URL = "https://qvapay.com/api"


def get_rates(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> List[Rate]:
    """Get current exchange rates."""
    with SyncClient(base_url=BASE_URL, timeout=timeout, follow_redirects=True) as client:
        response = client.get("rates/index")
        validate_response(response)
        return [Rate.from_json(item) for item in response.json()]


def get_coins(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> List[Coin]:
    """Get available coins."""
    with SyncClient(base_url=BASE_URL, timeout=timeout, follow_redirects=True) as client:
        response = client.get("coins")
        validate_response(response)
        return [Coin.from_json(item) for item in response.json()]


def get_p2p_coins_list(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> List[Coin]:
    """Get P2P enabled currencies."""
    with SyncClient(base_url=BASE_URL, timeout=timeout, follow_redirects=True) as client:
        response = client.get("p2p/get_coins_list")
        validate_response(response)
        return [Coin.from_json(item) for item in response.json()]


def get_p2p_pairs_average(
    coin: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT_CONFIG,
) -> dict:
    """Get P2P completed pairs average for a given coin."""
    with SyncClient(base_url=BASE_URL, timeout=timeout, follow_redirects=True) as client:
        response = client.get(
            "p2p/completed_pairs_average", params={"coin": coin.upper()}
        )
        validate_response(response)
        return response.json()
