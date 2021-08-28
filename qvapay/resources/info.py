import requests


class Info(object):
    """
    QvaPay app info
    """

    id = None
    user_id = None
    name = None
    url = None
    description = None
    callback = None
    logo = None
    active = None
    enabled = None

    def __init__(self, id, user_id, name, url, description, callback, logo, active, enabled):
        self.user_id = user_id
        self.name = name
        self.url = url
        self.description = description
        self.callback = callback
        self.logo = logo
        self.id = id
        self.active = active
        self.enabled = enabled
