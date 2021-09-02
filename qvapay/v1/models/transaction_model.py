from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TransactionModel(BaseModel):
    """
    QvaPay transaction
    """

    id: UUID = Field(alias="uuid")
    user_id: int
    app_id: int
    amount: float
    description: str
    remote_id: UUID
    status: str
    paid_by_user_id: int
    created_at: datetime
    updated_at: datetime
    signed: Optional[int]
