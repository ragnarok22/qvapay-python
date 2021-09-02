from typing import Optional

from pydantic import AnyUrl, BaseModel


class LinkModel(BaseModel):
    url: Optional[AnyUrl]
    label: str
    active: bool
