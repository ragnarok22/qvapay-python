from typing import Union

from httpx import (
    AsyncClient,  # noqa: F401
    Timeout,
)
from httpx import Client as BaseClient

TimeoutTypes = Union[Timeout, float, None]
DEFAULT_TIMEOUT = Timeout(5.0)
BASE_URL = "https://api.qvapay.com"
V2_BASE_URL = "https://api.qvapay.com/v2"


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()
