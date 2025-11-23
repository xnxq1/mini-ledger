from dataclasses import asdict

from app.domain.merchants import Merchant
from app.infra.db.repos.base import EntityRepo
from app.infra.db.repos.exceptions import EntityAlreadyExistsError
from app.logic.merchants.exceptions import MerchantAlreadyExistError
from app.logic.utils import convert_dt_to_dict


class MerchantsService:
    def __init__(
        self,
        merchants_repo: EntityRepo,
    ):
        self.merchants_repo = merchants_repo

    async def create_merchant(self, merchant: dict) -> dict:
        try:
            res = await self.merchants_repo.insert(payload=merchant)
        except EntityAlreadyExistsError as e:
            raise MerchantAlreadyExistError(str(e)) from e

        return asdict(res)

    async def get_merchants(self,) -> list:
        res = await self.merchants_repo.search()
        return convert_dt_to_dict(res)
