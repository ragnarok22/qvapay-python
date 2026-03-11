from typing import List

from ..http import BASE_URL, DEFAULT_TIMEOUT, AsyncClient, TimeoutTypes
from ..models.stock import Stock
from ..utils import validate_response


async def list(
    timeout: TimeoutTypes = DEFAULT_TIMEOUT,
) -> List[Stock]:
    """Get current stock/exchange data."""
    async with AsyncClient(
        base_url=BASE_URL,
        timeout=timeout,
        follow_redirects=True,
    ) as client:
        response = await client.get("stocks")
        validate_response(response)
        return [Stock.from_json(item) for item in response.json()]
