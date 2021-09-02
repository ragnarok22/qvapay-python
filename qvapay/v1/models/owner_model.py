from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class OwnerModel(BaseModel):
    id: UUID = Field(alias="uuid")
    username: str
    lastname: str
    name: str
    logo: str
    kyc: bool
    bio: Optional[str]
