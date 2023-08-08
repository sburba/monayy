import re
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import NewType

EMAIL_REGEX = re.compile(r"(?P<user>.+)@(?P<host>.+\..+)")


class EmailAddress:
    address: str
    user: str
    host: str

    def __init__(self, address: str):
        match = EMAIL_REGEX.match(address)
        if not match:
            raise ValueError(f"Invalid email address: {address}")
        self.address = address
        self.host = match.group("host")
        self.user = match.group("user")


UserId = NewType("UserId", uuid.UUID)
AccountId = NewType("AccountId", uuid.UUID)
EmailId = NewType("EmailId", uuid.UUID)


@dataclass
class User:
    id: UserId
    name: str
    email_id: str


class AccountType(Enum):
    SAVINGS = "savings"
    CHECKING = "checking"
    CREDIT = "credit"


class AccountDatasourceType(Enum):
    EMAIL = "email"
    SMS = "sms"


@dataclass
class AccountDatasource:
    type: AccountDatasourceType
    identifier: str
    discriminator: str | None = None


@dataclass
class Account:
    account_id: AccountId
    type: AccountType
    name: str
    datasources: list[AccountDatasource]
