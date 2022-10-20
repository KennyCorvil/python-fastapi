from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str ="default"
    database_port: str ="default"
    database_password: str ="default"
    database_name: str ="default"
    database_username: str ="default"
    secret_key: str ="default"
    algorithm: str ="dbkwru627r4fbreuoyfbyebf"
    access_token_expire_minutes: int = 60

    class Config:
        env_file = ".env"

settings = Settings()

