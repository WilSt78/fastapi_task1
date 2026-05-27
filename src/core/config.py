from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    ORIGINS: str = "http://localhost:3000"
    PORT: int = 8000
    ROOT_PATH: str = ""

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 10
    AUTH_ALGORITHM: str = "HS256"
    SECRET_KEY_AUTH: SecretStr

    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "postgres"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "fastapi"
    POSTGRES_PASSWORD: str
    POSTGRES_RECONNECT_INTERVAL_SEC: int = 1

    @property
    def postgres_url(self) -> str:
        url = f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return url

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


settings = Settings()
