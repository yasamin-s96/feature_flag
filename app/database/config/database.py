from pydantic_settings import BaseSettings, SettingsConfigDict


class PostgresSettings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_DEBUG_MODE: bool
    POOL_SIZE: int
    MAX_OVERFLOW: int
    POOL_RECYCLE: int
    POOL_PRE_PING: bool
    POOL_TIMEOUT: int
    FUTURE: bool
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


PostgresConfig = PostgresSettings()
