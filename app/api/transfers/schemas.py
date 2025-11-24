from decimal import Decimal

from pydantic import BaseModel, Field, model_validator


class CreateTransferRequest(BaseModel):
    from_merchant: str
    to_merchant: str
    amount: Decimal = Field(gt=0)
    currency: str

    @model_validator(mode="after")
    def validate_different_merchants(self):
        if self.from_merchant == self.to_merchant:
            raise ValueError("Cannot transfer to the same merchant")
        return self
