from dataclasses import dataclass
from uuid import UUID


@dataclass
class Owner:
    id: UUID
    username: str
    name: str
    lastname: str
    logo: str
    kyc: bool
    bio: str
