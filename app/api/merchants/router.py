from fastapi import APIRouter

from app.api.merchants.schemas import CreateBalanceRequest, CreateMerchantRequest
from app.api.schemas import OkResponse
from app.logic.factories import balance_service_factory, merchant_service_factory

router = APIRouter(prefix="/merchants", tags=["Merchants"])


@router.post("/")
async def create_merchant(payload: CreateMerchantRequest) -> OkResponse:
    merchant_service = merchant_service_factory()
    res = await merchant_service.create_merchant(payload.model_dump())
    return OkResponse(result=res)


@router.get("/")
async def get_merchants() -> OkResponse:
    merchant_service = merchant_service_factory()
    res = await merchant_service.get_merchants()
    return OkResponse(result=res)


@router.get("/{merchant_name}")
async def get_merchants_with_balances(merchant_name: str) -> OkResponse:
    merchant_service = merchant_service_factory()
    res = await merchant_service.get_merchants_with_balances(merchant_name=merchant_name)
    return OkResponse(result=res)


@router.get("/{merchant_name}/balance")
async def get_merchant_balances(merchant_name: str) -> OkResponse:
    balance_service = balance_service_factory()
    res = await balance_service.get_balances(merchant_name=merchant_name)
    return OkResponse(result=res)


@router.post("/balance")
async def create_balance(payload: CreateBalanceRequest) -> OkResponse:
    balance_service = balance_service_factory()
    res = await balance_service.create_balance(payload.model_dump())
    return OkResponse(result=res)
