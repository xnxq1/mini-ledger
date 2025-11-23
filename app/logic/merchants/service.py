from dataclasses import asdict

from app.infra.db.repos.balances import BalancesRepo
from app.infra.db.repos.exceptions import EntityAlreadyExistsError
from app.infra.db.repos.merchants import MerchantsRepo
from app.logic.merchants.exceptions import MerchantAlreadyExistError, MerchantDoesNotExistError
from app.logic.utils import convert_dt_to_dict


class MerchantsService:
    def __init__(
        self,
        merchants_repo: MerchantsRepo,
        balances_repo: BalancesRepo,
    ):
        self.merchants_repo = merchants_repo
        self.balances_repo = balances_repo

    async def create_merchant(self, merchant: dict) -> dict:
        try:
            res = await self.merchants_repo.insert(payload=merchant)
        except EntityAlreadyExistsError as e:
            raise MerchantAlreadyExistError(str(e)) from e

        return asdict(res)

    async def get_merchants_with_balances(self, merchant_name: str) -> dict:
        merchant = await self.merchants_repo.search_first_row(name=merchant_name, archived=False)
        if merchant is None:
            raise MerchantDoesNotExistError("Merchant not found")
        balances = await self.balances_repo.search(merchant_id=merchant.id, archived=False)
        return {**convert_dt_to_dict(merchant), "balances": convert_dt_to_dict(balances)}

    async def get_merchants(self) -> list:
        res = await self.merchants_repo.search(archived=False)
        return convert_dt_to_dict(res)
