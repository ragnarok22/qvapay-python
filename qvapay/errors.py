from dataclasses import dataclass


@dataclass
class QvaPayError(Exception):
    status_code: int
