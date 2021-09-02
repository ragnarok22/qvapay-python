from .info_model import InfoModel
from .owner_model import OwnerModel
from .paid_by_model import PaidByModel
from .transaction_model import TransactionModel


class TransactionDetailModel(TransactionModel):
    """
    QvaPay transaction
    """

    paid_by: PaidByModel
    app: InfoModel
    owner: OwnerModel
