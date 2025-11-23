from app.domain.merchants import Merchant
from app.infra.db.repos.base import EntityRepo
from app.infra.db.repos.exceptions import EntityAlreadyExistsError
from app.logic.merchants.exceptions import MerchantAlreadyExistError


class MerchantsService:
    def __init__(
        self,
        merchants_repo: EntityRepo,
    ):
        self.merchants_repo = merchants_repo

    async def create_merchant(self, merchant: dict) -> Merchant:
        try:
            res = await self.merchants_repo.insert(payload=merchant)
        except EntityAlreadyExistsError as e:
            raise MerchantAlreadyExistError(str(e)) from e

        return res
