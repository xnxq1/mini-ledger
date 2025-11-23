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
            result = result.fetchall()
            return [dict(r._mapping) for r in result]

    async def fetchrow(self, query) -> dict | None:
        async with self._connection() as conn:
            result = await conn.execute(query)
            result = result.fetchone()
            return dict(result._mapping) if result else None


class EntityRepo(BaseRepo):
    db_entity = None
    domain_entity = None

    def _get_filter_bool_expression(self, filter_name, filter_value):
        return self.db_entity.columns[filter_name].__eq__(filter_value)

    def _apply_filters(self, query, **filters):
        for filter_name, filter_value in filters.items():
            query = query.where(self._get_filter_bool_expression(filter_name, filter_value))

        return query

    @handle_db_errors
    async def search(self, **filters) -> list[domain_entity]:
        query = self._apply_filters(select(self.db_entity), **filters)
        res = await self.fetch(query)
        return [self.domain_entity(**r) for r in res]

    @handle_db_errors
    async def search_first_row(self, **filters) -> domain_entity:
        res = await self.search(**filters)
        return res[0] if res else None

    @handle_db_errors
    async def insert(self, payload: dict) -> domain_entity:
        query = self.db_entity.insert().values(payload).returning(self.db_entity)
        res = await self.fetchrow(query)
        return self.domain_entity(**res)
