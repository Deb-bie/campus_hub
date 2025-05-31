import enum
from sqlalchemy import Enum # type: ignore

class EventStatusEnum(enum.Enum):
    ACTIVE = "active"
    CANCELLED = "cancelled"
    RESCHEDULED = "rescheduled"
    ONHOLD = "onhold"
