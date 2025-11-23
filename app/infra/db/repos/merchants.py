from app.infra.db.models import merchants
from app.infra.db.repos.base import EntityRepo


class MerchantsRepo(EntityRepo):
    entity = merchants


