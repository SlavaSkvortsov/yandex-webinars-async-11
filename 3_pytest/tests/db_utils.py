from copy import deepcopy
from dataclasses import dataclass
from functools import cached_property

from pydantic import PostgresDsn
from sqlalchemy import text
from sqlalchemy.ext.asyncio import (
    AsyncEngine, create_async_engine,
)
from sqlalchemy.orm import DeclarativeMeta


@dataclass
class DBUtils:
    dsn: PostgresDsn

    @cached_property
    def postgres_engine(self) -> AsyncEngine:
        postgres_dsn = deepcopy(self.dsn)
        postgres_dsn.path = '/postgres'
        return create_async_engine(postgres_dsn, isolation_level='AUTOCOMMIT')

    @cached_property
    def db_engine(self) -> AsyncEngine:
        return create_async_engine(self.dsn, isolation_level='AUTOCOMMIT')

    async def create_database(self) -> None:
        query = text(f"CREATE DATABASE {self.dsn.path[1:]} ENCODING 'utf8'")
        async with self.postgres_engine.connect() as conn:
            await conn.execute(query)

    async def create_tables(self, base: DeclarativeMeta) -> None:
        async with self.db_engine.begin() as conn:
            await conn.run_sync(base.metadata.create_all)

    async def drop_database(self) -> None:
        query = text(f'DROP DATABASE {self.dsn.path[1:]}')
        async with self.postgres_engine.begin() as conn:
            await conn.execute(query)

    async def database_exists(self) -> bool:
        query = text('SELECT 1 FROM pg_database WHERE datname = :database')
        async with self.postgres_engine.connect() as conn:
            query_result = await conn.execute(query, {'database': self.dsn.path[1:]})
        result = query_result.scalar()
        return bool(result)


async def create_db(dsn: PostgresDsn, base: DeclarativeMeta) -> None:
    db_utils = DBUtils(dsn=dsn)

    try:
        if await db_utils.database_exists():
            await db_utils.drop_database()

        await db_utils.create_database()
        await db_utils.create_tables(base)
    finally:
        await db_utils.postgres_engine.dispose()
        await db_utils.db_engine.dispose()
