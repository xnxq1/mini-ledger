from dataclasses import asdict

from fastapi import APIRouter

from app.api.merchants.schemas import CreateMerchantRequest
from app.api.schemas import OkResponse
from app.logic.factories import merchant_service_factory

router = APIRouter(prefix="/merchants", tags=["Merchants"])


@router.post("/")
async def create_merchant(payload: CreateMerchantRequest) -> OkResponse:
    merchant_service = merchant_service_factory()
    res = await merchant_service.create_merchant(payload.model_dump())
    return OkResponse(result=asdict(res))
