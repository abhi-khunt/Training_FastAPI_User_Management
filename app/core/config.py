from pydantic_settings import BaseSettings
from pydantic import Field,SecretStr


class Settings(BaseSettings):
    database_url: str = Field(..., alias="DATABASE_URL")
    secret_key: SecretStr
    algorithm: str ="HS256"
    access_token_expire_minutes:int = 30
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
