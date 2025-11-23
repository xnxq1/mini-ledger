from dataclasses import asdict

from app.infra.db.repos.balances import BalancesRepo
from app.infra.db.repos.exceptions import EntityAlreadyExistsError, ForeignKeyViolationError
from app.infra.db.repos.merchants import MerchantsRepo
from app.logic.balances.exceptions import BalanceAlreadyExistError, BalanceMerchantDoesNotExistError
from app.logic.utils import normalize_dict


class BalancesService:
    def __init__(
        self,
        balance_repo: BalancesRepo,
        merchant_repo: MerchantsRepo,
    ):
        self.balance_repo = balance_repo
        self.merchant_repo = merchant_repo

    async def create_balance(self, balance: dict) -> dict:
        try:
            res = await self.balance_repo.insert(payload=balance)
        except EntityAlreadyExistsError as e:
            raise BalanceAlreadyExistError(str(e)) from e
        except ForeignKeyViolationError as e:
            raise BalanceMerchantDoesNotExistError("Merchant does not exist") from e

        return normalize_dict(asdict(res))

    async def get_balances(self, merchant_name: str) -> list:
        """
        Не можем сделать join запрос поскольку нужно зарейзить not found если нет мерчанта
        """
        merchant = await self.merchant_repo.search_first_row(name=merchant_name)
        if not merchant:
            raise BalanceMerchantDoesNotExistError("Merchant does not exist")
        return await self.balance_repo.search(merchant_id=merchant.id)
