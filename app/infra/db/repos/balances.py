from app.domain.balances import Balance
from app.infra.db.models import balances
from app.infra.db.repos.base import EntityRepo


class BalancesRepo(EntityRepo):
    db_entity = balances
    domain_entity = Balance