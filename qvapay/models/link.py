from dataclasses import dataclass
from typing import Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Link:
    url: Optional[str]
    label: str
    active: bool
