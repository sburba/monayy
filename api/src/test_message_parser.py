import datetime
import email.utils
import re

from src.message_parser import parse_message, Message
from src.transactions import DollarAmount

MESSAGE_REGEX = re.compile(
    r"Capital One: A chrge or hold for \$?(?P<amount_dollars>\d+)\.(?P<amount_cents>\d+) on (?P<date>.+) was placed"
    r" on your (?P<account>.+) at (?P<store>.+)\. Std carrier chrges apply"
)


def test_parse_message():
    transaction = parse_message(
        "Capital One: A chrge or hold for $105.22 on August 06, 2023 was placed on your SavorOne Credit Card ("
        "1234) at Safeway. Std carrier chrges apply",
        MESSAGE_REGEX
    )

    assert transaction == Message(
        datetime.datetime(2023, 8, 6),
        store='Safeway',
        discriminator='SavorOne Credit Card (1234)',
        amount=DollarAmount(10522),
    )
