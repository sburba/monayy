from typing import Annotated

from fastapi import Depends
from src.account.types import EmailId, User, UserId
from src.db.connection import db_transaction
from src.db.schema import user_table
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncConnection

USERS_BY_EMAIL_ID = {
    'test': User(
        id=UserId('user-one-id'),
        name='Sam',
        email_id='1df596d5-c4e7-4991-ad15-3c02046c0998'
    )
}


class UserNotFoundError(Exception):
    pass


class UserService:
    _db_conn: AsyncConnection

    def __init__(self, db_conn: Annotated[AsyncConnection, Depends(db_transaction)]):
        self._db_conn = db_conn

    async def find_by_email_id(self, email_id: EmailId) -> UserId:
        await self._db_conn.execute(select(user_table).where(User.email_id == email_id))
        user = USERS_BY_EMAIL_ID[email_id]
        if not user:
            raise UserNotFoundError(f"Unknown email id: {email_id}")
        return user
