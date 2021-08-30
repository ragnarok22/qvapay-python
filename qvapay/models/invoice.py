from dataclasses import dataclass, field
from uuid import UUID

from dataclasses_json import config, dataclass_json


@dataclass_json
@dataclass
class Invoice:
    """
    QvaPay invoice
    """

    app_id: UUID
    amount: float
    description: str
    remote_id: str
    signed = None
    transaction_uuid: UUID = field(metadata=config(field_name="transation_uuid"))
    url: str
    signed_url: str = field(metadata=config(field_name="signedUrl"))
