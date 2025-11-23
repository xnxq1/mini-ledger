from app.infra.db.repos.balances import BalancesRepo
from app.infra.db.repos.merchants import MerchantsRepo
from app.logic.balances.service import BalancesService
from app.logic.merchants.service import MerchantsService


def merchant_service_factory():
    return MerchantsService(
        merchants_repo=MerchantsRepo(),
    )

def balance_service_factory():
    return BalancesService(
        balance_repo=BalancesRepo(),
    )