from app.models.user import UserProfile
from app.schemas.user import UserProfileCreate
from sqlalchemy.orm import Session # type: ignore


class CrudUser:
    def create_user_profile(self, db: Session, *, obj_in: UserProfileCreate) -> UserProfile:
        # Create new user profile

        db_obj = UserProfile(
            user_id=obj_in.user_id,
            first_name = obj_in.first_name,
            last_name = obj_in.last_name,
            email = obj_in.email
        )
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        
        return db_obj

