import dataclasses
from decimal import Decimal
from uuid import UUID

from app.domain.base import BaseEntity


@dataclasses.dataclass
class Transfer(BaseEntity):
    from_merchant_id: UUID
    to_merchant_id: UUID
    amount: Decimal
    currency: str
    percent_fee: Decimal
    idempotency_key: str
