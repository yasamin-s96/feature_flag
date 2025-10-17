import urllib.parse

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker

from app.database.config.database import PostgresConfig

# Generate Database URL
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{PostgresConfig.DATABASE_USERNAME}:{urllib.parse.quote(PostgresConfig.DATABASE_PASSWORD)}"
    f"@{PostgresConfig.DATABASE_HOSTNAME}:{PostgresConfig.DATABASE_PORT}/{PostgresConfig.DATABASE_NAME}"
)

# Create Database Engine
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=PostgresConfig.DATABASE_DEBUG_MODE,
    future=PostgresConfig.FUTURE,
    pool_size=PostgresConfig.POOL_SIZE,
    max_overflow=PostgresConfig.MAX_OVERFLOW,
    pool_pre_ping=PostgresConfig.POOL_PRE_PING,
    pool_recycle=PostgresConfig.POOL_RECYCLE,
    pool_timeout=PostgresConfig.POOL_TIMEOUT,
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


def get_session_maker() -> async_sessionmaker:
    return session_maker


async def async_connection():
    async with session_maker() as session:
        yield session
