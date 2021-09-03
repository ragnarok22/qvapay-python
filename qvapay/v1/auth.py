from dataclasses import dataclass, field
from os import environ

from dotenv import load_dotenv

load_dotenv()


@dataclass
class QvaPayAuth:
    qvapay_app_id: str = field(default=environ["QVAPAY_APP_ID"])
    qvapay_app_secret: str = field(default=environ["QVAPAY_APP_SECRET"])
