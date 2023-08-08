import uuid
from typing import AsyncGenerator

import pytest_asyncio
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from testing.postgresql import Postgresql

from src.db.connection import setup as db_setup, teardown as db_teardown, db_transaction_context
from src.db.schema import metadata, datasource_type_table, account_type_table


@pytest_asyncio.fixture(scope="session")
async def test_db():
    pass

@pytest_asyncio.fixture
async def test_db_conn(test_db) -> AsyncGenerator[AsyncConnection, None]:
    await db_setup("sqlite+aiosqlite:///:memory:")
    async with db_transaction_context() as conn:
        await conn.run_sync(metadata.create_all)
        await conn.execute(insert(datasource_type_table).values([
            {"id": uuid.uuid4(), "name": "email"},
            {"id": uuid.uuid4(), "name": "sms"}
        ]))
        await conn.execute(insert(account_type_table).values([
            {"id": uuid.uuid4(), "name": "checking"},
            {"id": uuid.uuid4(), "name": "savings"},
            {"id": uuid.uuid4(), "name": "credit"},
        ]))
        try:
            yield conn
        except:
            pass
    await db_teardown()
