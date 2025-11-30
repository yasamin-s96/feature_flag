from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_DEBUG: bool = False
    BASE_URL: AnyHttpUrl
    HOST: str
    PORT: str
    DEFAULT_LOCALE: str
    WORKER: int
    ORIGINS: list[str]

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow"
    }


class DatabaseSettings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DEBUG_MODE: bool
    POOL_SIZE: int
    POOL_RECYCLE: int
    POOL_PRE_PING: bool
    POOL_TIMEOUT: int
    MAX_OVERFLOW: int
    FUTURE: bool

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow"
    }

class RedisSettings(BaseSettings):
    REDIS_HOST: str
    REDIS_PORT: str
    TTL: int
    REDIS_PASSWORD: str = ""

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow"
    }


class SecuritySettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    APP_KEY: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow"
    }

class CoreSettings(BaseSettings):
    HOST: str
    PORT: int
    ENVIRONMENT: str
    LOCAL_STORAGE_PATH: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
        "extra": "allow"
    }

class Settings:
    app: AppSettings = AppSettings()
    database: DatabaseSettings = DatabaseSettings()
    redis: RedisSettings = RedisSettings()
    security: SecuritySettings = SecuritySettings()
    core: CoreSettings = CoreSettings()


settings = Settings()