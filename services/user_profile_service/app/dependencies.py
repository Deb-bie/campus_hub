from fastapi import Depends, Header, HTTPException, status # type: ignore
from sqlalchemy.orm import Session # type: ignore
from app.models.user import UserProfile
from app.db.base import SessionLocal
from app.config import settings


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        x_user_email: str = Header(..., alias="x-user-email"),
        db: Session = Depends(get_db)
) -> UserProfile:    
    user = db.query(UserProfile).filter(UserProfile.email == x_user_email).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user