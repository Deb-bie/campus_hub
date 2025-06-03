from fastapi import APIRouter, Depends # type: ignore
from app.crud.users import CrudUser
from app.dependencies import get_current_user, get_db
from app.schemas.user import UserProfileCreate, UserProfileResponse
from app.models.user import UserProfile
from sqlalchemy.orm import Session # type: ignore

router = APIRouter()

# create user
@router.post("/", response_model=UserProfileResponse, description="Create User Profile")
async def create_user_profile(
    user_in: UserProfileCreate,
    db: Session = Depends(get_db)
):
    crud_user = CrudUser()
    user_profile = crud_user.create_user_profile(db=db, obj_in=user_in)
    return user_profile


# get current user profile
@router.get("/me", response_model=UserProfileResponse, description="Get current user profile")
async def get_current_user_profile(
    current_user: UserProfile = Depends(get_current_user),

):
    return current_user
