from fastapi import Depends, HTTPException, status # type: ignore
from fastapi.security import OAuth2PasswordBearer # type: ignore
from sqlalchemy.orm import Session # type: ignore
from jose import jwt, JWTError # type: ignore
from app.models.user import UserProfile
from app.db.base import SessionLocal
from app.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
) -> UserProfile:
    
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate crendential",
        headers={"WWW-Authenticate": "Bearer"},
    )


    try:
        payload = jwt.decode(
            token=token,
            key=settings.JWT__SECRET__KEY,
            options={"verify_signature": True, "verify_aud": False},
            algorithms=[settings.ALGORITHM]
        )

        email: str = payload.get("sub")

        if email is None:
            raise credentials_exception
        
        
    
    except JWTError as e:
        raise credentials_exception
    
    user = db.query(UserProfile).filter(UserProfile.email == email).first()

    if user is None:
        raise credentials_exception
    
    return user