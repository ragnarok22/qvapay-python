from pydantic import BaseSettings


class QvaPayAuth(BaseSettings):
    qvapay_app_id: str
    qvapay_app_secret: str

    class Config:
        env_file = ".env"
