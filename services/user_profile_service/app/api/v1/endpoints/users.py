from fastapi import APIRouter, Depends, HTTPException, Header # type: ignore
from app.crud.users import CrudUser
from app.dependencies import get_current_user, get_db
from app.schemas.user import UserProfileCreate, UserProfileResponse, UserProfileUpdate
from app.models.user import UserProfile
from app.clients.auth_service_client import AuthServiceClient
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


@router.get("/all", response_model=list[UserProfileResponse], description="Get all users")
async def get_all_users(
    db: Session = Depends(get_db)
):
    users = db.query(UserProfile).all()
    return users



# get user using user id
@router.get("/id/{user_id}", response_model=UserProfileResponse, description="Get user profile by id")
async def get_user_profile(
    user_id,
    db: Session = Depends(get_db)
):
    user = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# get user by email
@router.get("/email/{user_email}", response_model=UserProfileResponse, description="Get user profile by email")
async def get_user_profile_by_email(
    user_email: str,
    db: Session = Depends(get_db)
):
    user = db.query(UserProfile).filter(UserProfile.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/update/{user_id}", response_model=UserProfileResponse, description="Update user profile ")
async def update_user(
    user_id, 
    user_in: UserProfileUpdate, 
    db: Session = Depends(get_db),
    user_email = Header(..., alias='x-user-email'),
    auth_header = Header(..., alias='authorization')
):
    current_user = get_current_user(user_email, db)
    print(current_user.user_id)

    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized user"
        )

    if not auth_header:
        raise HTTPException(
            status_code=401, 
            detail="Unauthorized - Missing headers"
        )
    
    token = auth_header.replace("Bearer ", "")
    user = db.query(UserProfile).filter(UserProfile.user_id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="User not found"
        )
    
    # Backup old data before update, for potential rollback
    original_data = {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email,
        "bio": user.bio
    }

    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        db.commit()
        db.refresh(user)

        user_profile_update_response= UserProfileResponse.from_orm(user)
        data = user_profile_update_response.model_dump(mode="json")

        auth_client = AuthServiceClient()
        await auth_client.update_user(user_id, data, token)

    except Exception as e:
        print("Auth service call failed, reverting local changes:", e)
        
        for field, value in original_data.items():
            setattr(user, field, value)

        db.commit()

        raise HTTPException(
            status_code=500, 
            detail="Failed to sync with Auth Service. Local update reverted."
        )

    return user_profile_update_response

