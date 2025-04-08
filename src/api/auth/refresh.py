from fastapi import (
    APIRouter,
    Request,
    Response,
    HTTPException,
    status
)
from jose import JWTError , jwt
from src.core.config import settings
from datetime import datetime , timedelta
from src.utils.auth import create_access_token


refresh_router = APIRouter()


@refresh_router.post("/refresh")
async def refresh(
    request: Request,
    response: Response
):
    refresh_token = request.get("refresh_token")
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token missing"
        )
    
    try:
        payload = jwt.decode(
            refresh_token,
            settings.REFRESH_SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        exp = payload.get("exp")

        if exp and datetime.utcnow().timestamp() > exp:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                datetime = "Refresh token expired"
            )
        
        new_access_token = await create_access_token(
            {
                "sub": payload["sub"]
            },
            timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )

        access_expire = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)


        response.set_cookie(
            key="access_token",
            value=new_access_token,
            httponly=True,
            max_age=int(access_expire.total_seconds())
        )

        return {"message": "Token refreshed"}
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )