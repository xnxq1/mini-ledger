from dataclasses import asdict

from app.infra.db.repos.balances import BalancesRepo
from app.infra.db.repos.exceptions import EntityAlreadyExistsError, ForeignKeyViolationError
from app.infra.db.repos.merchants import MerchantsRepo
from app.logic.balances.exceptions import BalanceAlreadyExistError, BalanceMerchantDoesNotExistError
from app.logic.utils import normalize_dict


class BalancesService:
    def __init__(
        self,
        balances_repo: BalancesRepo,
        merchants_repo: MerchantsRepo,
    ):
        self.balances_repo = balances_repo
        self.merchants_repo = merchants_repo

    async def create_balance(self, balance: dict) -> dict:
        try:
            res = await self.balances_repo.insert(payload=balance)
        except EntityAlreadyExistsError as e:
            raise BalanceAlreadyExistError(str(e)) from e
        except ForeignKeyViolationError as e:
            raise BalanceMerchantDoesNotExistError("Merchant does not exist") from e

        return normalize_dict(asdict(res))

    async def get_balances(self, merchant_name: str) -> list:
        merchant = await self.merchants_repo.search_first_row(name=merchant_name, archived=False)
        if not merchant:
            raise BalanceMerchantDoesNotExistError("Merchant does not exist")
        balances = await self.balances_repo.search(merchant_id=merchant.id, archived=False)
        return [normalize_dict(asdict(balance)) for balance in balances]
