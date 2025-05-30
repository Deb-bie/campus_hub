import enum
from sqlalchemy import Enum # type: ignore

class CategoryEnum(enum.Enum):
    CULTURAL_DIVERSITY = "cultural & diversity"
    ACADEMIC = "academic"
    SOCIAL_ENTERTAINMENT = "social & entertainment"
    SPORTS_FITNESS = "sports & fitness"
    CAREER_PROFESSIONAL_DEVELOPMENT = "career & professional development"
    HEALTH_WELLNESS = "health & wellness"
    CLUBS_ORGANIZATIONS = "clubs & organizations"
    RESIDENTIAL_LIFE = "residential life"
    MONEY_FINANCE = "money & finance"

