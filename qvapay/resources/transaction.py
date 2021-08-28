import requests


class Transaction(object):
    """
    QvaPay transaction
    """

    id = None
    user_id = None
    amount = None
    description = None
    remote_id = None
    status = None
    paid_by_user_id = None
    signed = None
    created_at = None
    updated_at = None
    paid_by = None
    # app_id
    # owner

    def __init__(
        self,
        id,
        user_id,
        amount,
        description,
        remote_id,
        status,
        paid_by_user_id,        
        created_at,
        updated_at,
        signed=None,
        paid_by=None
    ):
        self.id = id
        self.user_id = user_id
        self.amount = amount
        self.description = description
        self.remote_id = remote_id
        self.status = status
        self.paid_by_user_id = paid_by_user_id
        self.signed = signed
        self.created_at = created_at
        self.updated_at = updated_at
        self.paid_by = paid_by


class PaginatedTransactions(object):

    transactions = []
    current_page = None
    last_page = None    

    def __init__(self, transactions=[], current_page=None, last_page=None):
        self.transactions = transactions
        self.current_page = current_page
        self.last_page = last_page
