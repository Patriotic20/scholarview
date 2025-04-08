from fastapi import APIRouter , Depends, HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from src.schemas.user import UserCreate ,  UserResponse
from sqlalchemy.exc import SQLAlchemyError 
from src.utils.auth import get_user
from src.models.user import User
from src.utils.auth import hash_password


signup_router = APIRouter()


@signup_router.post("/signup" , response_model=UserResponse)
async def signup(
    user_item: UserCreate,
    db: AsyncSession = Depends(get_db)):

    existing_user = get_user(db=db , username=user_item.username)

    if not  existing_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        

    user_data = user_item.model_dump(exclude_unset=True)
    user_data["password"] = await hash_password(user_data["password"])

    new_user = User(**user_data)

    try:
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e} "
        )
    
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}"
        )
    
    return new_user



    