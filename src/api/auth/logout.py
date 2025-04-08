from fastapi import APIRouter , Request , Response , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db


logout_router = APIRouter()


@logout_router.post("/logout")
async def logout(
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )

    response.delete_cookie(
        key="refresh_token",
        httponly=True,
        secure=True,
        samesite="lax"
    )
    
    return {"message": "Successfully logged out"}