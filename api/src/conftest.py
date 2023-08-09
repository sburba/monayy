import asyncio
import os
import uuid
from typing import AsyncGenerator

import pytest
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from testing.postgresql import Postgresql

from src.db.connection import setup as db_setup, teardown as db_teardown, db_transaction_context
from src.db.schema import metadata, datasource_type_table, account_type_table


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_db():
    pass


@pytest.fixture
async def test_db_conn(test_db) -> AsyncGenerator[AsyncConnection, None]:
    await db_setup(os.getenv("TEST_DB_URL"))
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
