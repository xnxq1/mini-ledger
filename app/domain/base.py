import dataclasses
import datetime
from uuid import UUID


@dataclasses.dataclass
class BaseEntity:
    id: UUID
    created: datetime
    updated: datetime
    archived: bool
