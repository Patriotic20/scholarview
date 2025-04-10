from fastapi import APIRouter , Depends , HTTPException , status , Response
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from fastapi.security import OAuth2PasswordRequestForm
from src.utils.auth import authenticate_user , create_access_token , create_refresh_token
from datetime import timedelta
from src.core.config import settings


login_router = APIRouter()


@login_router.post("/login")
async def login(
    response : Response,
    from_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)):
    

    user = await authenticate_user(db=db , username=from_data.username , password=from_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid username and password"
        )
    
    access_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_expire = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    
    access_token = await create_access_token(
        {
            "sub": user.username
        },
        access_expire
    )

    refresh_token = await create_refresh_token(
        {
            "sub": user.username
        },
        refresh_expire
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        max_age=int(access_expire.total_seconds()),
        samesite="lax"
    )

    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=int(refresh_expire.total_seconds()),
        samesite="lax"
    )
    
    return {
        "message": "Login successful",
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }
