from typing import Any, List

from ..http import BASE_URL, DEFAULT_TIMEOUT, AsyncClient, TimeoutTypes
from ..utils import validate_response


def _client(timeout: TimeoutTypes) -> AsyncClient:
    return AsyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
    )


async def list(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[Any]:
    """Get current stock/exchange data."""
    async with _client(timeout) as client:
        response = await client.get("stocks/index")
        validate_response(response)
        return response.json()
