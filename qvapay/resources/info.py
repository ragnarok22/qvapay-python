from dataclasses import dataclass


@dataclass
class Info(object):
    """
    QvaPay app info
    """

    id: str = None
    user_id: int = None
    name: str = None
    url: str = None
    description: str = None
    callback: str = None
    logo: str = None
    active: bool = False
    enabled: bool = False

    def __post_init__(self):
        if self.active == 1:
            self.active = True
        if self.enabled == 1:
            self.enabled = True
