import uuid

import pytest
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncConnection

from .schema import user_table


@pytest.mark.asyncio
async def test_schema(test_db: AsyncConnection):
    await test_db.execute(
        insert(user_table).values(id=uuid.uuid4(), name="Bob Builder", email_id=uuid.uuid4())
    )
    results = (await test_db.execute(select(user_table.c.name))).all()
    assert results == [("Bob Builder",)]
