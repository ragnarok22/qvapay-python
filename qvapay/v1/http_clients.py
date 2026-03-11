from typing import Union

from httpx import (
    AsyncClient,  # noqa: F401
    Timeout,
)
from httpx import Client as BaseClient  # noqa: F401

TimeoutTypes = Union[Timeout, float, None]
DEFAULT_TIMEOUT = Timeout(5.0)


class SyncClient(BaseClient):
    def aclose(self) -> None:
        self.close()
