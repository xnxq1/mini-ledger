from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, Field, model_validator


class CreateMerchantRequest(BaseModel):
    name: str
    percent_fee: Decimal = Field(gt=0, le=100)

    @model_validator(mode="after")
    def validate_different_merchants(self):
        if self.from_merchant == self.to_merchant:
            raise ValueError("Cannot transfer to the same merchant")
        return self


class CreateBalanceRequest(BaseModel):
    merchant_id: UUID
    currency: str
    amount: Decimal = Field(alias="initial_amount", ge=0)
