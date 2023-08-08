from dataclasses import dataclass
from typing import NewType, Annotated
import uuid

from fastapi import Depends
from sqlalchemy import insert, select, literal
from sqlalchemy.ext.asyncio import AsyncConnection

from src.account.types import AccountDatasourceType
from src.db.connection import db_transaction
from src.db.schema import incoming_messages_table, datasource_type_table

IncomingMessageId = NewType("IncomingMessageId", uuid.UUID)


@dataclass
class IncomingMessage:
    id: IncomingMessageId
    type: AccountDatasourceType
    from_addr: str
    to_addr: str
    text: str


class IncomingMessageService:
    _db: AsyncConnection

    def __init__(self, db: Annotated[AsyncConnection, Depends(db_transaction)]):
        self._db = db

    async def queue_incoming_email(
        self, from_addr: str, to_addr: str, text: str
    ) -> IncomingMessageId:
        select_type_id = select(
            literal(uuid.uuid4()),
            literal(from_addr),
            literal(to_addr),
            literal(text),
            datasource_type_table.c.id,
        ).where(datasource_type_table.c.name == AccountDatasourceType.EMAIL.value)
        results = await self._db.stream(
            insert(incoming_messages_table)
            .from_select(
                ["id", "from_addr", "to_addr", "text", "datasource_type"],
                select_type_id,
            )
            .returning(incoming_messages_table.c.id)
        )
        result = await anext(results)

        return IncomingMessageId(result.id)

    async def fetch_queue(self) -> list[IncomingMessage]:
        raw_messages = await self._db.stream(
            select(
                incoming_messages_table.c.id,
                incoming_messages_table.c.from_addr,
                incoming_messages_table.c.to_addr,
                incoming_messages_table.c.text,
                datasource_type_table.c.name.label("datasource_type"),
            ).join(
                datasource_type_table,
                incoming_messages_table.c.datasource_type == datasource_type_table.c.id,
            )
        )
        return [
            IncomingMessage(
                raw_message.id,
                AccountDatasourceType(raw_message.datasource_type),
                raw_message.from_addr,
                raw_message.to_addr,
                raw_message.text,
            )
            async for raw_message in raw_messages
        ]

    async def acquire_entries(self, entry_count: int = 5) -> list[IncomingMessage]:
        raw_messages = await self._db.stream(
            select(
                incoming_messages_table.c.id,
                incoming_messages_table.c.from_addr,
                incoming_messages_table.c.to_addr,
                incoming_messages_table.c.text,
                datasource_type_table.c.name.label("datasource_type"),
            )
            .join(
                datasource_type_table,
                incoming_messages_table.c.datasource_type == datasource_type_table.c.id,
            )
            .with_for_update(skip_locked=True)
            .order_by(incoming_messages_table.c.id)
            .fetch(entry_count)
        )

        return [
            IncomingMessage(
                raw_message.id,
                AccountDatasourceType(raw_message.datasource_type),
                raw_message.from_addr,
                raw_message.to_addr,
                raw_message.text,
            )
            async for raw_message in raw_messages
        ]
