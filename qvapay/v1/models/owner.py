from dataclasses import dataclass
from typing import Any, Optional
from uuid import UUID


@dataclass
class Owner:
    id: UUID  # alias: uuid
    username: str
    lastname: str
    name: str
    logo: str
    kyc: bool
    bio: Optional[str]

    def __post_init__(self):
        self.id = UUID(str(self.id))
        self.username = str(self.username)
        self.lastname = str(self.lastname)
        self.name = str(self.name)
        self.logo = str(self.logo)
        self.kyc = bool(str(self.kyc))
        self.bio = str(self.bio) if self.bio is not None else None

    @staticmethod
    def from_json(json: Any) -> "Owner":
        json["id"] = json["uuid"]
        del json["uuid"]
        return Owner(**json)
