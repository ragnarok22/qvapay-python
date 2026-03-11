from typing import List

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
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[CoinCategory]:
    """Get available coins (v2 format)."""
    async with _client(timeout) as client:
        response = await client.get("v2/coins")
        validate_response(response)
        return [CoinCategory.from_json(item) for item in response.json()]


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
