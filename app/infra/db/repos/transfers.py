from app.domain.transfers import Transfer
from app.infra.db.models import transfers
from app.infra.db.repos.base import EntityRepo


class TransfersRepo(EntityRepo):
    db_entity = transfers
    domain_entity = Transfer
