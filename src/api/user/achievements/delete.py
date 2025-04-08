from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from src.models.achievements import Achievement
from sqlalchemy.future import select

delete_router = APIRouter()


@delete_router.delete("/delete")
async def delete(
    achievements_id: int,
    db: AsyncSession = Depends(get_db)):
    
    result = await db.execute(select(Achievement).where(Achievement.id == achievements_id))
    achievements_data = result.scalars().first()

    if not  achievements_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Not found achievement"
        )
    
    await db.delete(achievements_data)
    await db.commit()

    return {"message" : "Achievements delete"}