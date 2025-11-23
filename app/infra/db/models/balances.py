from sqlalchemy import NUMERIC, Column, ForeignKey, Index, String, Table

from app.infra.db.utils import get_base_fields, metadata

balances = Table(
    "balances",
    metadata,
    *get_base_fields(),
    Column("merchant_id", ForeignKey("merchants.id", name="merchants_id_fk"), nullable=False),
    Column("currency", String, nullable=False),
    Column("amount", NUMERIC(precision=12, scale=8), nullable=False, server_default="0"),
    Index("balances_merchant_id_uq_idx", "merchant_id", "currency", unique=True),
)
