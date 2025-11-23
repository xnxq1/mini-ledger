from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    postgres_db: str = Field(default="mini_ledger", alias="POSTGRES_DB")
    postgres_user: str = Field(default="ledger_user", alias="POSTGRES_USER")
    postgres_password: str = Field(default="ledger_password", alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(default="postgres", alias="POSTGRES_HOST")
    postgres_port: int = Field(default=5432, alias="POSTGRES_PORT")

    redis_host: str = Field(default="redis", alias="REDIS_HOST")
    redis_port: int = Field(default=6379, alias="REDIS_PORT")
    redis_db: int = Field(default=0, alias="REDIS_DB")

    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    json_logs: bool = Field(default=False, alias="JSON_LOGS")

    debug: bool = Field(default=False, alias="DEBUG")
    app_name: str = Field(default="Mini Ledger", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    pythonunbuffered: int = Field(default=1, alias="PYTHONUNBUFFERED")

    @computed_field
    @property
    def db_url(self) -> str:
        return (
            f"postgresql://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    @computed_field
    @property
    def redis_url(self) -> str:
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


def get_settings() -> Settings:
    return Settings()


settings = get_settings()
