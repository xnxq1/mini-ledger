import dataclasses
from uuid import UUID

from app.domain.base import BaseEntity


@dataclasses.dataclass
class Balance(BaseEntity):
    merchant_id: UUID
    currency: str
