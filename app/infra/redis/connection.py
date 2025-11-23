import redis.asyncio as redis
from redis.asyncio import Redis

from app.infra.config import settings
from app.infra.logging import get_logger

logger = get_logger(__name__)

_redis_client: Redis | None = None


async def get_redis_client() -> Redis:
    global _redis_client

    if _redis_client is None:
        logger.info("Creating Redis connection", redis_url=settings.redis_url)

        _redis_client = await redis.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=20,
        )

    return _redis_client


async def close_redis() -> None:
    global _redis_client

    if _redis_client is not None:
        logger.info("Closing Redis connection")
        await _redis_client.close()
        _redis_client = None
        logger.info("Redis connection closed")
