from fastapi import APIRouter, Header

from app.api.schemas import OkResponse
from app.api.transfers.schemas import CreateTransferRequest
from app.logic.factories import transfer_service_factory

router = APIRouter(prefix="/transfers", tags=["Transfers"])


@router.post("/")
async def create_transfer(
    payload: CreateTransferRequest,
    idempotency_key: str = Header(alias="Idempotency-Key"),
) -> OkResponse:
    transfer_service = transfer_service_factory()
    res = await transfer_service.create_transfer(
        payload=payload.model_dump(), idempotency_key=idempotency_key
    )
    return OkResponse(result=res)
