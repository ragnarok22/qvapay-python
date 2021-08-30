from dataclasses import dataclass, field
from uuid import UUID

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class Owner:
    id: UUID = field(metadata=config(field_name="uuid"))
    username: str
    name: str
    lastname: str
    logo: str
    kyc: bool
    bio: str
