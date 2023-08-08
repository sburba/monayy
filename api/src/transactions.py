import datetime
from dataclasses import dataclass
from typing import NewType, Union

from src.account.types import Account

StoreId = NewType('AccountId', str)


@dataclass
class DollarAmount:
    cents: int


@dataclass
class Store:
    id: StoreId
    name: str


@dataclass
class Charge:
    date: datetime.datetime
    store: StoreId
    from_account: Account
    amount: DollarAmount


@dataclass
class Transfer:
    date: datetime.datetime
    from_account: Account
    to_account: Account
    amount: DollarAmount


Transaction = Union[Charge, Transfer]
