import abc
from contextlib import asynccontextmanager

from sqlalchemy import select

from app.infra.db.connection import get_async_engine
from app.infra.db.repos.exceptions import handle_db_errors


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
            result = result.fetchone()
            return dict(result._mapping) if result else None


class EntityRepo(BaseRepo):
    db_entity = None
    domain_entity = None

    @handle_db_errors
    async def search(self) -> list[domain_entity]:
        query = select(self.db_entity)
        res = await self.fetch(query)
        return [self.domain_entity(**r) for r in res]

    @handle_db_errors
    async def insert(self, payload: dict) -> domain_entity:
        query = self.db_entity.insert().values(payload).returning(self.db_entity)
        res = await self.fetchrow(query)
        return self.domain_entity(**res)
