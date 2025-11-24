from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field


class CreateMerchantRequest(BaseModel):
    name: str
    percent_fee: Decimal = Field(gt=0, le=100)


class CreateBalanceRequest(BaseModel):
    merchant_id: UUID
    currency: str
    amount: Decimal = Field(alias="initial_amount", ge=0)
