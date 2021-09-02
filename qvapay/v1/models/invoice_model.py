from uuid import UUID

from pydantic import AnyUrl, BaseModel, Field


class InvoiceModel(BaseModel):
    """
    QvaPay invoice
    """

    app_id: UUID
    transation_id: UUID = Field(alias="transation_uuid")
    amount: float
    description: str
    remote_id: str
    signed: int
    url: AnyUrl
    signed_url: AnyUrl = Field(alias="signedUrl")
