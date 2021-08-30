from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class Info:
    """
    QvaPay app info
    """

    id: UUID = field(metadata=config(field_name="uuid"))
    user_id: int
    name: str
    url: str
    desc: str
    callback: str
    success_url: str
    cancel_url: str
    logo: str
    active: bool = field(metadata=config(decoder=bool))
    enabled: bool = field(metadata=config(decoder=bool))
    card: int
    created_at: datetime = field(metadata=config(decoder=str))
    updated_at: datetime = field(metadata=config(decoder=str))
