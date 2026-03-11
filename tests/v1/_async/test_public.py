from httpx import Timeout
from pytest import mark as pytest_mark

from qvapay.v1._async.public import (
    get_coins,
    get_p2p_coins_list,
    get_p2p_pairs_average,
    get_rates,
)

TIMEOUT = 20


@pytest_mark.anyio
async def test_get_rates():
    rates = await get_rates(timeout=Timeout(TIMEOUT))
    assert isinstance(rates, list)


@pytest_mark.anyio
async def test_get_coins():
    coins = await get_coins(timeout=Timeout(TIMEOUT))
    assert isinstance(coins, list)


@pytest_mark.anyio
async def test_get_p2p_coins_list():
    coins = await get_p2p_coins_list(timeout=Timeout(TIMEOUT))
    assert isinstance(coins, list)


@pytest_mark.anyio
async def test_get_p2p_pairs_average():
    result = await get_p2p_pairs_average("BTC", timeout=Timeout(TIMEOUT))
    assert isinstance(result, dict)
