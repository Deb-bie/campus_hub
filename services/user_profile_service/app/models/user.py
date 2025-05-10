import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean # type: ignore
from sqlalchemy.ext.declarative import declarative_base # type: ignore


# Create a base class for declarative models
Base = declarative_base()


class UserProfile(Base):
    __tablename__ = "user"

    id = Column(
        uuid,
        primary_key=True,
        index=True
    )

    first_name = Column(
        String,
        nullable=False
    )

    last_name = Column(
        String,
        nullable=False
    )

    email = Column(
        String,
        nullable=False,
        unique=True,
        index=True
    )

    password = Column(
        String,
        nullable=False
    )

    created_at = Column(
        datetime
    )

    updated_at = Column(
        datetime
    )

    last_loggedIn = Column(
        datetime
    )


