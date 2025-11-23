import abc
from contextlib import asynccontextmanager

from sqlalchemy import select

from app.infra.db.connection import get_async_engine


class BaseRepo(abc.ABC):

    @asynccontextmanager
    async def _connection(self):
        engine = get_async_engine()
        async with engine.begin() as conn:
            yield conn

    @asynccontextmanager
    async def transaction(self):
        async with self._connection() as con:
            async with con.transaction():
                yield con

    async def fetch(self, query) -> list:
        async with self._connection() as conn:
            result = await conn.execute(query)
            return result.fetchall()

    async def fetchrow(self, query) -> dict | None:
        async with self._connection() as conn:
            result = await conn.execute(query)
            return result.fetchone()


class EntityRepo(BaseRepo):
    entity = None

    async def search(self) -> list:
        query = select(self.entity)
        return await self.fetch(query)