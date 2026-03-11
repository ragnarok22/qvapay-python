from httpx import Timeout

from qvapay.v1._sync.public import (
    get_coins,
    get_p2p_coins_list,
    get_p2p_pairs_average,
    get_rates,
)

TIMEOUT = 20


def test_get_rates():
    rates = get_rates(timeout=Timeout(TIMEOUT))
    assert isinstance(rates, list)


def test_get_coins():
    coins = get_coins(timeout=Timeout(TIMEOUT))
    assert isinstance(coins, list)


def test_get_p2p_coins_list():
    coins = get_p2p_coins_list(timeout=Timeout(TIMEOUT))
    assert isinstance(coins, list)


def test_get_p2p_pairs_average():
    result = get_p2p_pairs_average("BTC", timeout=Timeout(TIMEOUT))
    assert isinstance(result, dict)
