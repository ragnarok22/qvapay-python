from typing import List, Optional

from ..http import BASE_URL, DEFAULT_TIMEOUT, AsyncClient, TimeoutTypes
from ..models.coin import Coin, CoinCategory
from ..utils import validate_response


def _client(timeout: TimeoutTypes) -> AsyncClient:
    return AsyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
    )


async def list(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[CoinCategory]:
    """Get available coins grouped by category."""
    async with _client(timeout) as client:
        response = await client.get("coins")
        validate_response(response)
        return [CoinCategory.from_json(item) for item in response.json()]


async def list_v2(
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
    async with _client(timeout) as client:
        response = await client.get("coins/v2", params=params)
        validate_response(response)
        return [Coin.from_json(item) for item in response.json()]


async def get(
    coin_id: int,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> Coin:
    """Get a specific coin by ID."""
    async with _client(timeout) as client:
        response = await client.get(f"coins/{coin_id}")
        validate_response(response)
        return Coin.from_json(response.json())


async def history(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> list:
    """Get coins price history."""
    async with _client(timeout) as client:
        response = await client.get("coins/history")
        validate_response(response)
        return response.json()
