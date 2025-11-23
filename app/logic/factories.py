from app.infra.db.repos.merchants import MerchantsRepo
from app.logic.merchants.service import MerchantsService


def merchant_service_factory():
    return MerchantsService(
        merchants_repo=MerchantsRepo(),
    )
