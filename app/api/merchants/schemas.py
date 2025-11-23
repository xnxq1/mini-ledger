from decimal import Decimal

from pydantic import BaseModel


class CreateMerchantRequest(BaseModel):
    name: str
    percent_fee: Decimal


