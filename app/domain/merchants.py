import dataclasses
from decimal import Decimal

from app.domain.base import BaseEntity


@dataclasses.dataclass
class Merchant(BaseEntity):
    name: str
    percent_fee: Decimal
