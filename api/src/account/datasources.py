from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import select

from fastapi import Depends

from src.account.types import AccountDatasourceType, UserId, EmailId, AccountDatasource
from src.db.connection import db_transaction
from src.db.schema import user_table, user_account_table, account_datasource_table, datasource_type_table
from typing import Annotated


class DatasourceService:
    _db_conn: AsyncConnection

    def __init__(self, db_conn: Annotated[AsyncConnection, Depends(db_transaction)]):
        self._db_conn = db_conn

    async def find_by_email_id(self, email_id: EmailId, datasource_type: AccountDatasourceType) -> list[AccountDatasource]:
        raw_datasources = await self._db_conn.stream(
            select(
                account_datasource_table.c.identifier.label("identifier"),
                account_datasource_table.c.discriminator.label("discriminator"),
                datasource_type_table.c.name.label("type")
            )
            .join(user_account_table, user_table.c.id == user_account_table.c.user_id)
            .join(account_datasource_table, user_account_table.c.account_id == account_datasource_table.c.account_id)
            .join(datasource_type_table, account_datasource_table.c.type == datasource_type_table.c.id)
            .where(user_table.c.email_id == email_id, datasource_type_table.c.name == datasource_type.value)
        )

        datasources = [AccountDatasource(
            AccountDatasourceType(raw_datasource.type),
            raw_datasource.identifier,
            raw_datasource.discriminator
        ) async for raw_datasource in raw_datasources]

        return datasources
