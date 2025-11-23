from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from app.infra.config import settings
from app.infra.logging import get_logger

logger = get_logger(__name__)

_engine: AsyncEngine | None = None


def get_async_engine() -> AsyncEngine:
    global _engine

    if _engine is None:
        db_url = settings.db_url.replace("postgresql://", "postgresql+asyncpg://")

        logger.info("Creating async engine with asyncpg", db_url=db_url.split("@")[-1])

        _engine = create_async_engine(
            db_url,
            echo=settings.debug,
            pool_size=20,
            max_overflow=10,
            pool_pre_ping=True,
            pool_recycle=3600,
        )

    return _engine


async def close_db() -> None:
    global _engine

    if _engine is not None:
        logger.info("Closing database connections")
        await _engine.dispose()
        _engine = None
        logger.info("Database connections closed")
