class QvaPayError(Exception):
    def __init__(self, status_code: int, *args: object) -> None:
        super().__init__(*args)
        self.status_code = status_code
