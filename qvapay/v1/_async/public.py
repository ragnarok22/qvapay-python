from typing import List

from ..http_clients import DEFAULT_TIMEOUT, AsyncClient, TimeoutTypes
from ..models.coin import CoinCategory
from ..utils import validate_response

BASE_URL = "https://qvapay.com/api"


def _client(timeout: TimeoutTypes) -> AsyncClient:
    return AsyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
    )


async def get_coins(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[CoinCategory]:
    """Get available coins grouped by category."""
    async with _client(timeout) as client:
        response = await client.get("coins")
        validate_response(response)
        return [CoinCategory.from_json(item) for item in response.json()]


async def get_p2p_pairs_average(
    coin: str,
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> float:
    """Get P2P completed pairs average for a given coin."""
    async with _client(timeout) as client:
        response = await client.get(
            "p2p/completed_pairs_average",
            params={"coin": coin.upper()},
        )
        validate_response(response)
        return float(response.text)
