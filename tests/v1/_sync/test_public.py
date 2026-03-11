from httpx import Timeout

from qvapay.v1._sync.public import get_coins, get_p2p_pairs_average

TIMEOUT = 20


def test_get_coins():
    categories = get_coins(timeout=Timeout(TIMEOUT))
    assert isinstance(categories, list)
    if categories:
        assert categories[0].name
        assert isinstance(categories[0].coins, list)


def test_get_p2p_pairs_average():
    result = get_p2p_pairs_average("BTC", timeout=Timeout(TIMEOUT))
    assert isinstance(result, float)
