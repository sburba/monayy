from sqlalchemy import MetaData, Table, Column, String, ForeignKey, Integer, UniqueConstraint, Text
from sqlalchemy_utils import UUIDType

metadata = MetaData()

# We use UUIDs for identifiers everywhere. Theoretically on insert this is slow, we should consider a uuid7 variant or
# similar that is time-sortable in the database and allows for faster insert
user_table = Table(
    "user",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("name", String(256), nullable=False),
    Column("email_id", UUIDType(binary=False), nullable=False, unique=True)
)

account_type_table = Table(
    "account_type",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("name", String(256), nullable=False)
)

account_table = Table(
    "account",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("name", String(256), nullable=False),
    Column("type", ForeignKey("account_type.id"), nullable=False)
)

user_account_table = Table(
    "user_account",
    metadata,
    Column("user_id", ForeignKey("user.id"), nullable=False),
    Column("account_id", ForeignKey("account.id"), nullable=False),
    UniqueConstraint("user_id", "account_id", name="unique_user_account")
)

datasource_type_table = Table(
    "datasource_type",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("name", String(256), nullable=False),
)

account_datasource_table = Table(
    "account_datasource",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("account_id", ForeignKey("account.id"), nullable=False),
    Column("type", ForeignKey("datasource_type.id"), nullable=False),
    Column("identifier", String(256), nullable=False),
    Column("discriminator", String(256)),
)

charge_category_table = Table(
    "charge_category",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("name", String(256), nullable=False, unique=True)
)

merchant_table = Table(
    "merchant",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("name", String(256), nullable=False, unique=True),
    Column("default_category", ForeignKey("charge_category.id")),
)

charge_table = Table(
    "charge",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("merchant", ForeignKey("merchant.id"), nullable=False),
    Column("category", ForeignKey("charge_category.id")),
    Column("amount_cents", Integer(), nullable=False),
)

transfer_table = Table(
    "transfer",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("from_account", ForeignKey("account.id"), nullable=False),
    Column("to_account", ForeignKey("account.id"), nullable=False),
    Column("amount_cents", Integer(), nullable=False),
)

incoming_messages_table = Table(
    "incoming_message",
    metadata,
    Column("id", UUIDType(binary=False), primary_key=True),
    Column("from_addr", String(512), nullable=False),
    Column("to_addr", String(512), nullable=False),
    Column("text", Text(), nullable=False),
    Column("datasource_type", ForeignKey("datasource_type.id"), nullable=False),
)
