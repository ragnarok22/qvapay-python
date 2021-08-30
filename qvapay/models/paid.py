from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class PaidBy:
    username: str
    name: str
    logo: str
