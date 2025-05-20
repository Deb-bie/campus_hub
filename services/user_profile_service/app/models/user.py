import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore
from sqlalchemy.dialects.postgresql import UUID # type: ignore


# Create a base class for declarative models
Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user_profile"

    user_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )

    email = Column(
        String
    )

    first_name = Column(
        String,
        nullable=False
    )

    last_name = Column (
        String,
        nullable=False
    )

    bio = Column(
        String
    )

    created_at = Column(
        DateTime,
        default=datetime.now(),
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
        nullable=False
    )
