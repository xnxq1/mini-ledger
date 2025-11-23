import dataclasses
from decimal import Decimal
from uuid import UUID

from app.domain.base import BaseEntity


@dataclasses.dataclass
class Balance(BaseEntity):
    merchant_id: UUID
    currency: str
    amount: Decimal
