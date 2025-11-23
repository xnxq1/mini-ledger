from decimal import Decimal

from app.infra.db.repos.balances import BalancesRepo
from app.infra.db.repos.merchants import MerchantsRepo
from app.infra.db.repos.transfers import TransfersRepo
from app.infra.redis.lock import RedisLocks
from app.logic.transfers.exceptions import (
    TransferBalanceDoesNotExistError,
    TransferInsufficientFundsError,
    TransferMerchantDoesNotExistError,
)
from app.logic.transfers.models import CreateTransferDict
from app.logic.utils import convert_dt_to_dict


class TransferService:
    def __init__(
        self,
        merchants_repo: MerchantsRepo,
        balances_repo: BalancesRepo,
        transfers_repo: TransfersRepo,
        redis_locks: RedisLocks,
    ):
        self.merchants_repo = merchants_repo
        self.balances_repo = balances_repo
        self.transfers_repo = transfers_repo
        self.redis_locks = redis_locks

    async def create_transfer(self, payload: CreateTransferDict, idempotency_key: str) -> dict:
        from_merchant_name = payload["from_merchant"]
        to_merchant_name = payload["to_merchant"]
        currency = payload["currency"]
        amount = payload["amount"]

        async with (
            self.redis_locks.acquire(
                key=f"merchant_balance_{from_merchant_name}_{currency}_transfer_lock", timeout=60
            ),
            self.redis_locks.acquire(
                key=f"merchant_balance_{to_merchant_name}_{currency}_transfer_lock", timeout=60
            ),
        ):
            exist_transfer = await self.transfers_repo.search_first_row(
                idempotency_key=idempotency_key
            )
            if exist_transfer:
                return convert_dt_to_dict(exist_transfer)

            from_merchant, to_merchant = await self.get_from_to_merchants(
                from_merchant_name, to_merchant_name
            )
            if not from_merchant or not to_merchant:
                raise TransferMerchantDoesNotExistError(
                    "From merchant or to merchant does not exist"
                )

            from_merchant_balance, to_merchant_balance = await self.get_from_to_merchant_balances(
                from_merchant.id, to_merchant.id, currency
            )

            if not from_merchant_balance:
                raise TransferBalanceDoesNotExistError(
                    f"From merchant balance with currency {currency} does not exist"
                )
            final_amount = amount + (amount / Decimal("100") * from_merchant.percent_fee)

            if from_merchant_balance.amount < final_amount:
                raise TransferInsufficientFundsError("Insufficient funds")

            async with self.transfers_repo.transaction():
                if not to_merchant_balance:
                    to_merchant_balance = await self.balances_repo.insert(
                        payload={
                            "merchant_id": to_merchant.id,
                            "currency": currency,
                            "amount": 0,
                        }
                    )
                await self.balances_repo.update_by_id(
                    entity_id=to_merchant_balance.id,
                    amount=to_merchant_balance.amount + amount,
                )
                await self.balances_repo.update_by_id(
                    entity_id=from_merchant_balance.id,
                    amount=from_merchant_balance.amount - final_amount,
                )
                transfer = await self.transfers_repo.insert(
                    payload={
                        "from_merchant_id": from_merchant.id,
                        "to_merchant_id": to_merchant.id,
                        "amount": amount,
                        "percent_fee": from_merchant.percent_fee,
                        "currency": currency,
                        "idempotency_key": idempotency_key,
                    }
                )

            return convert_dt_to_dict(transfer)

    async def get_from_to_merchants(self, from_merchant_name: str, to_merchant_name: str) -> tuple:
        merchants = await self.merchants_repo.search(name_in=[from_merchant_name, to_merchant_name])
        from_merchant = [m for m in merchants if m.name == from_merchant_name]
        to_merchant = [m for m in merchants if m.name == to_merchant_name]

        return from_merchant[0] if from_merchant else None, to_merchant[0] if to_merchant else None

    async def get_from_to_merchant_balances(
        self, from_merchant_id: str, to_merchant_id: str, currency: str
    ) -> tuple:
        balances = await self.balances_repo.search(
            merchant_id_in=[from_merchant_id, to_merchant_id],
            currency=currency,
        )
        from_balance = [b for b in balances if b.merchant_id == from_merchant_id]

        to_balance = [b for b in balances if b.merchant_id == to_merchant_id]

        return from_balance[0] if from_balance else None, to_balance[0] if to_balance else None
