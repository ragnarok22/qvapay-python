from dataclasses import dataclass, field
from os import environ

from .errors import QvaPayError


@dataclass
class QvaPayAuth:
    uuid: str = field(default_factory=lambda: environ.get("QVAPAY_UUID", ""))
    secret_key: str = field(
        default_factory=lambda: environ.get("QVAPAY_SECRET_KEY", "")
    )

    def __post_init__(self):
        if not self.uuid and not self.secret_key:
            raise QvaPayError(0, "QVAPAY_UUID and QVAPAY_SECRET_KEY are not set")
        elif not self.uuid:
            raise QvaPayError(0, "QVAPAY_UUID is not set")
        elif not self.secret_key:
            raise QvaPayError(0, "QVAPAY_SECRET_KEY is not set")


@dataclass
class QvaPayUserAuth:
    access_token: str

    def __post_init__(self):
        if not self.access_token:
            raise QvaPayError(0, "access_token is not set")
