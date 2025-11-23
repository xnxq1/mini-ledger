import dataclasses
from decimal import Decimal

from sqlalchemy import and_, select

from app.domain.base import BaseEntity
from app.domain.transfers import Transfer
from app.infra.db.models import merchants, transfers
from app.infra.db.repos.base import EntityRepo


@dataclasses.dataclass
class TransferWithMerchant(BaseEntity):
    from_merchant: str
    to_merchant: str
    amount: Decimal
    percent_fee: Decimal
    currency: str
    idempotency_key: str


class TransfersRepo(EntityRepo):
    db_entity = transfers
    domain_entity = Transfer

    async def get_transfers_with_merchant_names(
        self,
        from_merchant: str | None = None,
        to_merchant: str | None = None,
        currency: str | None = None,
    ) -> list[TransferWithMerchant]:
        from_m = merchants.alias("from_merchant")
        to_m = merchants.alias("to_merchant")

        query = (
            select(
                transfers.c.id,
                transfers.c.created,
                transfers.c.updated,
                transfers.c.archived,
                from_m.c.name.label("from_merchant"),
                to_m.c.name.label("to_merchant"),
                transfers.c.amount,
                transfers.c.percent_fee,
                transfers.c.currency,
                transfers.c.idempotency_key,
            )
            .select_from(
                transfers.join(from_m, transfers.c.from_merchant_id == from_m.c.id).join(
                    to_m, transfers.c.to_merchant_id == to_m.c.id
                )
            )
            .where(
                transfers.c.archived.is_(False),
                from_m.c.archived.is_(False),
                to_m.c.archived.is_(False),
            )
        )

        query = self._apply_transfer_filters(
            query, from_m, to_m, from_merchant, to_merchant, currency
        )

        res = await self.fetch(query)
        return [TransferWithMerchant(**r) for r in res]

    def _apply_transfer_filters(
        self,
        query,
        from_m,
        to_m,
        from_merchant: str | None,
        to_merchant: str | None,
        currency: str | None,
    ):
        filters = []

        if from_merchant:
            filters.append(from_m.c.name == from_merchant)
        if to_merchant:
            filters.append(to_m.c.name == to_merchant)
        if currency:
            filters.append(transfers.c.currency == currency)

        if filters:
            query = query.where(and_(*filters))

        return query
