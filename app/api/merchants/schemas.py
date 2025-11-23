from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer


class CreateMerchantRequest(BaseModel):
    name: str
    percent_fee: Decimal = Field(gt=0)

class CreateBalanceRequest(BaseModel):
    merchant_id: UUID
    currency: str
    amount: Decimal = Field(alias="initial_amount", ge=0)



