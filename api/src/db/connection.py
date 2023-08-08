from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from .schema import metadata

_engine: AsyncEngine | None = None


async def setup(connection_str: str):
    global _engine
    _engine = create_async_engine(connection_str, echo=True)
    async with db_transaction_context() as conn:
        await conn.run_sync(metadata.create_all)


async def teardown():
    global _engine
    if _engine is not None:
        await _engine.dispose()
        _engine = None


class DbNotConnectedError(Exception):
    pass


async def db_transaction() -> AsyncIterator[AsyncConnection]:
    if _engine is None:
        raise DbNotConnectedError()

    async with _engine.begin() as conn:
        yield conn


db_transaction_context = asynccontextmanager(db_transaction)
