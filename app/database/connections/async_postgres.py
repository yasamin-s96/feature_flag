import urllib.parse

from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from app.core.settings import settings

# Generate Database URL
DATABASE_URL = (
    f"postgresql+asyncpg://"
    f"{settings.database.DATABASE_USERNAME}:{urllib.parse.quote(settings.database.DATABASE_PASSWORD)}"
    f"@{settings.database.DATABASE_HOSTNAME}:{settings.database.DATABASE_PORT}/{settings.database.DATABASE_NAME}"
)

# Create Database Engine
engine: AsyncEngine = create_async_engine(
    DATABASE_URL,
    echo=settings.database.DEBUG_MODE,
    future=settings.database.FUTURE,
    pool_size=settings.database.POOL_SIZE,
    max_overflow=settings.database.MAX_OVERFLOW,
    pool_pre_ping=settings.database.POOL_PRE_PING,
    pool_recycle=settings.database.POOL_RECYCLE,
    pool_timeout=settings.database.POOL_TIMEOUT,
)

session_maker = async_sessionmaker(engine, expire_on_commit=False)


def get_session_maker() -> async_sessionmaker:
    return session_maker


async def async_connection():
    async with session_maker() as session:
        yield session
