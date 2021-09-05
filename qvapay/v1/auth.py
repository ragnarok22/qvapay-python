from dataclasses import dataclass, field
from os import environ

from dotenv import load_dotenv

from .errors import QvaPayError

load_dotenv()


@dataclass
class QvaPayAuth:
    qvapay_app_id: str = field(default=environ["QVAPAY_APP_ID"])
    qvapay_app_secret: str = field(default=environ["QVAPAY_APP_SECRET"])

    def __post_init__(self):
        if not self.qvapay_app_id and not self.qvapay_app_secret:
            raise QvaPayError(0, "QVAPAY_APP_ID and QVAPAY_APP_SECRET are not setted")
        elif not self.qvapay_app_id:
            raise QvaPayError(0, "QVAPAY_APP_ID is not setted")
        elif not self.qvapay_app_secret:
            raise QvaPayError(0, "QVAPAY_APP_SECRET is not setted")
