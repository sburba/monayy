import uuid

import pytest
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy import insert

from src.account.datasources import DatasourceService
from src.account.types import AccountDatasource, AccountDatasourceType, EmailId
from src.db.schema import user_table, account_table, account_type_table, user_account_table, account_datasource_table, \
    datasource_type_table


@pytest.mark.asyncio
async def test_find_by_email_id(test_db: AsyncConnection):
    user_id = uuid.uuid4()
    account_id = uuid.uuid4()
    account_type_id = uuid.uuid4()
    email_id = uuid.uuid4()
    datasource_type_id = uuid.uuid4()
    await test_db.execute(insert(user_table).values(id=user_id, name="Bob", email_id=email_id))
    await test_db.execute(insert(account_type_table).values(id=account_type_id, name="Checking"))
    await test_db.execute(insert(account_table).values(id=account_id, name="Bob's Account", type=account_type_id))
    await test_db.execute(insert(user_account_table).values(user_id=user_id, account_id=account_id))
    await test_db.execute(insert(datasource_type_table).values(id=datasource_type_id, name="email"))
    await test_db.execute(insert(account_datasource_table).values(
        id=uuid.uuid4(), account_id=account_id, type=datasource_type_id, identifier="test@example.com")
    )
    datasources = DatasourceService(test_db)
    sources = await datasources.find_by_email_id(EmailId(email_id), datasource_type=AccountDatasourceType.EMAIL)
    assert sources == [AccountDatasource(type=AccountDatasourceType.EMAIL, identifier="test@example.com")]
