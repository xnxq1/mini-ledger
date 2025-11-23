from typing import Annotated

from fastapi import APIRouter, Header, Query

from app.api.schemas import OkResponse
from app.api.transfers.schemas import CreateTransferRequest
from app.logic.factories import transfer_service_factory

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.post("/")
async def create_transfer(
    payload: CreateTransferRequest,
    idempotency_key: str = Header(alias="Idempotency-Key", min_length=1),
) -> OkResponse:
    transfer_service = transfer_service_factory()
    res = await transfer_service.create_transfer(
        payload=payload.model_dump(), idempotency_key=idempotency_key
    )
    return OkResponse(result=res)


@router.get("/")
async def get_transfers(
    from_merchant: Annotated[str | None, Query(alias="from")] = None,
    to_merchant: Annotated[str | None, Query(alias="to")] = None,
    currency: str | None = None,
) -> OkResponse:
    transfer_service = transfer_service_factory()
    res = await transfer_service.get_transfers(
        from_merchant=from_merchant,
        to_merchant=to_merchant,
        currency=currency,
    )
    return OkResponse(result=res)
