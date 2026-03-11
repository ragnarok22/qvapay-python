from typing import Union

from httpx import AsyncClient  # noqa: F401
from httpx import Client as BaseClient
from httpx import Timeout

TimeoutTypes = Union[Timeout, float, None]
DEFAULT_TIMEOUT = Timeout(5.0)
BASE_URL = "https://api.qvapay.com"


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()
