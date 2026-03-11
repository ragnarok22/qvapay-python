from dataclasses import dataclass, field
from os import environ

from dotenv import load_dotenv

from .errors import QvaPayError

load_dotenv()


@dataclass
class QvaPayAuth:
    qvapay_app_id: str = field(default_factory=lambda: environ.get("QVAPAY_APP_ID", ""))
    qvapay_app_secret: str = field(
        default_factory=lambda: environ.get("QVAPAY_APP_SECRET", "")
    )

    def __post_init__(self):
        if not self.qvapay_app_id and not self.qvapay_app_secret:
            raise QvaPayError(0, "QVAPAY_APP_ID and QVAPAY_APP_SECRET are not set")
        elif not self.qvapay_app_id:
            raise QvaPayError(0, "QVAPAY_APP_ID is not set")
        elif not self.qvapay_app_secret:
            raise QvaPayError(0, "QVAPAY_APP_SECRET is not set")


@dataclass
class QvaPayUserAuth:
    access_token: str

    def __post_init__(self):
        if not self.access_token:
            raise QvaPayError(0, "access_token is not set")
