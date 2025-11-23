from sqlalchemy import NUMERIC, Column, ForeignKey, Index, String, Table

from app.infra.db.utils import get_base_fields, metadata

transfers = Table(
    "transfers",
    metadata,
    *get_base_fields(),
    Column(
        "from_merchant_id",
        ForeignKey("merchants.id", name="transfers_from_merchants_id_fk"),
        nullable=False,
    ),
    Column(
        "to_merchant_id",
        ForeignKey("merchants.id", name="transfers_to_merchants_id_fk"),
        nullable=False,
    ),
    Column("amount", NUMERIC(precision=12, scale=2), nullable=False),
    Column("percent_fee", NUMERIC(precision=12, scale=2), nullable=False),
    Column("currency", String, nullable=False),
    Index("transfers_from_merchant_id_idx", "from_merchant_id"),
    Index("transfers_to_merchant_id_idx", "to_merchant_id"),
)
