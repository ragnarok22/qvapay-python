import requests


class Invoice(object):
    """
    QvaPay invoice
    """

    amount = None
    description = None
    remote_id = None
    signed = None
    id = None
    url = None
    signed_url = None

    def __init__(self, amount, description, remote_id, signed, id, url, signed_url):
        self.amount = amount
        self.description = description
        self.remote_id = remote_id
        self.signed = signed
        self.id = id
        self.url = url
        self.signed_url = signed_url
