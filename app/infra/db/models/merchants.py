from sqlalchemy import NUMERIC, Column, String, Table

from app.infra.db.utils import get_base_fields, metadata

merchants = Table(
    "merchants",
    metadata,
    *get_base_fields(),
    Column("name", String, nullable=False),
    Column("percent_fee", NUMERIC(precision=12, scale=2), nullable=False),
)
