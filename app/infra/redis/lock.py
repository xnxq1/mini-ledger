from contextlib import asynccontextmanager

from app.infra.logging import get_logger
from app.infra.redis.connection import get_redis_client

logger = get_logger(__name__)


class RedisLocks:
    @asynccontextmanager
    async def acquire(self, key, timeout: int = None):
        redis_conn = await get_redis_client()
        async with redis_conn.lock(key, timeout=timeout):
            yield
