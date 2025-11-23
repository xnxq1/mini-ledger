from decimal import Decimal

from pydantic import BaseModel, Field


class CreateTransferRequest(BaseModel):
    from_merchant: str
    to_merchant: str
    amount: Decimal = Field(gt=0)
    currency: str
