import uuid

from sqlalchemy.ext.asyncio import AsyncConnection

from src.account.types import AccountDatasourceType
from src.incoming.incoming_messages import (
    IncomingMessageService,
    IncomingMessage,
)

import pytest


@pytest.mark.asyncio
async def test_incoming_messages(test_db: AsyncConnection):
    s = IncomingMessageService(test_db)
    idOne = await s.queue_incoming_email(
        from_addr="from_addr_one@example.com", to_addr="to_addr_one@example.com", text="text one"
    )
    idTwo = await s.queue_incoming_email(
        from_addr="from_addr_two@example.com", to_addr="to_addr_two@example.com", text="text two"
    )
    assert await s.acquire_entries(1) == [
        IncomingMessage(
            idOne,
            AccountDatasourceType.EMAIL,
            from_addr="from_addr_one@example.com",
            to_addr="to_addr_one@example.com",
            text="text one",
        ),
    ]
    assert await s.acquire_entries(1) == [
        IncomingMessage(
            idTwo,
            AccountDatasourceType.EMAIL,
            from_addr="from_addr_two@example.com",
            to_addr="to_addr_two@example.com",
            text="text two"
        )
    ]
