from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class Info:
    """
    QvaPay app info
    """

    uuid: UUID
    user_id: int
    name: str
    url: str
    desc: str
    callback: str
    success_url: str
    cancel_url: str
    logo: str
    active: bool
    enabled: bool
    card: int
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        if self.active == 1:
            self.active = True
        else:
            self.active = False
        if self.enabled == 1:
            self.enabled = True
        else:
            self.enabled = False
