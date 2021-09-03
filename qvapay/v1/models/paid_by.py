from dataclasses import dataclass
from typing import Any


@dataclass
class PaidBy:
    username: str
    name: str
    logo: str

    def __post_init__(self):
        self.username = str(self.username)
        self.name = str(self.name)
        self.logo = str(self.logo)

    @staticmethod
    def from_json(json: Any) -> "PaidBy":
        return PaidBy(**json)
