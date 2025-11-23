from app.infra.db.repos.balances import BalancesRepo
from app.infra.db.repos.merchants import MerchantsRepo
from app.infra.db.repos.transfers import TransfersRepo
from app.infra.redis.lock import RedisLocks
from app.logic.balances.service import BalancesService
from app.logic.merchants.service import MerchantsService
from app.logic.transfers.service import TransferService


def merchant_service_factory():
    return MerchantsService(
        merchants_repo=MerchantsRepo(),
        balances_repo=BalancesRepo(),
    )


def balance_service_factory():
    return BalancesService(
        balances_repo=BalancesRepo(),
        merchants_repo=MerchantsRepo(),
    )


def transfer_service_factory():
    return TransferService(
        balances_repo=BalancesRepo(),
        merchants_repo=MerchantsRepo(),
        transfers_repo=TransfersRepo(),
        redis_locks=RedisLocks(),
    )
