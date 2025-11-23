from app.domain.merchants import Merchant
from app.infra.db.models import merchants
from app.infra.db.repos.base import EntityRepo


class MerchantsRepo(EntityRepo):
    db_entity = merchants
    domain_entity = Merchant
