from dataclasses import asdict
from decimal import Decimal

from app.infra.db.repos.base import EntityRepo
from app.infra.db.repos.exceptions import EntityAlreadyExistsError, ForeignKeyViolationError
from app.logic.balances.exceptions import BalanceAlreadyExistError, BalanceMerchantDoesNotExistError


class BalancesService:
    def __init__(
        self,
        balance_repo: EntityRepo,
    ):
        self.balance_repo = balance_repo

    def _normalize_decimal(self, value):
        if isinstance(value, Decimal):
            return f"{value:.8f}"
        return value

    def _normalize_dict(self, data: dict) -> dict:
        return {
            key: self._normalize_decimal(value)
            for key, value in data.items()
        }
    async def create_balance(self, balance: dict) -> dict:
        try:
            res = await self.balance_repo.insert(payload=balance)
        except EntityAlreadyExistsError as e:
            raise BalanceAlreadyExistError(str(e)) from e
        except ForeignKeyViolationError as e:
            raise BalanceMerchantDoesNotExistError('Merchant does not exist') from e

        return self._normalize_dict(asdict(res))

