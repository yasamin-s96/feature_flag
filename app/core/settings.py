from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class AppSettings(BaseSettings):
    APP_NAME: str
    APP_DESCRIPTION: str
    APP_VERSION: str
    APP_DEBUG: bool = False
    BASE_URL: AnyHttpUrl
    DEFAULT_LOCALE: str
    WORKER: int
    ORIGINS: list[str]


class DatabaseSettings(BaseSettings):
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    DATABASE_HOSTNAME: str
    DATABASE_PORT: int
    DATABASE_DEBUG_MODE: bool
    POOL_SIZE: int
    POOL_RECYCLE: int
    POOL_PRE_PING: bool
    POOL_TIMEOUT: int
    MAX_OVERFLOW: int
    FUTURE: bool


class RedisSettings(BaseSettings):
    HOST: str
    PORT: int
    PASSWORD: str | None = None
    TTL: int

    model_config = SettingsConfigDict(env_prefix="REDIS_")



class SecuritySettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    APP_KEY: str


class CoreSettings(BaseSettings):
    HOST: str
    PORT: int
    ENVIRONMENT: str
    LOCAL_STORAGE_PATH: str


# class Settings:
#     # app: AppSettings = AppSettings()
#     database: DatabaseSettings = DatabaseSettings()
#     redis: RedisSettings = RedisSettings()
#     security: SecuritySettings = SecuritySettings()
#     core: CoreSettings = CoreSettings()

    # model_config = SettingsConfigDict(env_file=f".env.{os.getenv('ENV', 'development')}")



settings = DatabaseSettings()