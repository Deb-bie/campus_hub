import enum
from sqlalchemy import Enum # type: ignore

class CategoryEnum(enum.Enum):
    CULTURAL = "cultural"
    ACADEMIC = "academic"
    SOCIAL = "social"
    SPORTS = "sports"
    CAREER = "career"
    HEALTH = "health"
    WORKSHOP = "workshop"
    FINANCE = "finance"
    OTHER = "other"

