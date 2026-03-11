from httpx import Timeout
from pytest import mark as pytest_mark

from qvapay.v1._async.public import get_coins, get_p2p_pairs_average

TIMEOUT = 20


@pytest_mark.anyio
async def test_get_coins():
    categories = await get_coins(timeout=Timeout(TIMEOUT))
    assert isinstance(categories, list)
    if categories:
        assert categories[0].name
        assert isinstance(categories[0].coins, list)


@pytest_mark.anyio
async def test_get_p2p_pairs_average():
    result = await get_p2p_pairs_average("BTC", timeout=Timeout(TIMEOUT))
    assert isinstance(result, float)
