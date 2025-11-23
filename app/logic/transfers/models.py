from decimal import Decimal
from typing import TypedDict


class CreateTransferDict(TypedDict):
    from_merchant: str
    to_merchant: str
    amount: Decimal
    currency: str
