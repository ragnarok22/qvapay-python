from pydantic import BaseModel


class PaidByModel(BaseModel):
    username: str
    name: str
    logo: str
