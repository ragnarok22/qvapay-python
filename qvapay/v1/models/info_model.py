from datetime import datetime
from uuid import UUID

from pydantic import AnyUrl, BaseModel, Field


class InfoModel(BaseModel):
    """
    QvaPay app info
    """

    id: UUID = Field(alias="uuid")
    user_id: int
    name: str
    url: AnyUrl
    description: str = Field(alias="desc")
    callback: str
    success_url: AnyUrl
    cancel_url: AnyUrl
    logo: str
    active: bool
    enabled: bool
    card: int
    created_at: datetime
    updated_at: datetime
