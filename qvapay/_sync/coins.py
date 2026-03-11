from typing import List, Optional

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
    *,
    enabled_in: Optional[bool] = None,
    enabled_out: Optional[bool] = None,
    enabled_p2p: Optional[bool] = None,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[Coin]:
    """Get operational coins with optional filtering."""
    params: dict = {}
    if enabled_in is not None:
        params["enabled_in"] = str(enabled_in).lower()
    if enabled_out is not None:
        params["enabled_out"] = str(enabled_out).lower()
    if enabled_p2p is not None:
        params["enabled_p2p"] = str(enabled_p2p).lower()
    with _client(timeout) as client:
        response = client.get("coins/v2", params=params)
        validate_response(response)
        return [Coin.from_json(item) for item in response.json()]


def get(
    coin_id: int,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> Coin:
    """Get a specific coin by ID."""
    with _client(timeout) as client:
        response = client.get(f"coins/{coin_id}")
        validate_response(response)
        return Coin.from_json(response.json())


def price_history(
    tick: str,
    *,
    timeframe: str = "24H",
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> list:
    """Get price history for a coin by ticker."""
    with _client(timeout) as client:
        response = client.get(
            f"coins/price-history/{tick}", params={"timeframe": timeframe}
        )
        validate_response(response)
        return response.json()
