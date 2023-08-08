import re
from dataclasses import dataclass
from datetime import datetime

import dateparser

from src.transactions import DollarAmount

AMOUNT_REGEX = re.compile(r"(\d+)\.(\d+)")


class UnexpectedMessageError(Exception):
    def __init__(self, message: str, message_text: str):
        super().__init__(f"error: {message}, full message text: {message_text}")


@dataclass
class Message:
    date: datetime
    store: str
    discriminator: str
    amount: DollarAmount


def parse_message(message: str, message_format: re.Pattern) -> Message:
    match = message_format.match(message)
    if not match:
        raise UnexpectedMessageError("Unexpected message format", message)

    amount_dollars = match.group('amount_dollars')
    amount_cents = match.group('amount_cents')
    try:
        amount = DollarAmount(int(amount_dollars) * 100 + int(amount_cents))
    except ValueError:
        raise UnexpectedMessageError(f"Unexpected amount format: ${amount_dollars}.{amount_cents}", message)

    date_str = match.group('date')
    date = dateparser.parse(date_str)
    if date is None:
        raise UnexpectedMessageError(f"Unexpected date format: {date_str}", message)
    store = match.group('store')
    discriminator = match.group('account')
    return Message(
        date=date,
        store=store,
        discriminator=discriminator,
        amount=amount,
    )
