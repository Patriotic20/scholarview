from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.base import get_db
from src.schemas.achievement import AchievementResponse
from src.models.achievements import Achievement
from typing import List

read_router = APIRouter()

@read_router.get("/get-all", response_model=List[AchievementResponse])
async def get_all_achievements(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Achievement).limit(10))
    achievements = result.scalars().all()

    if not achievements:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No achievements found"
        )

    return achievements


@read_router.get("/get/{achievement_id}", response_model=AchievementResponse)
async def get_achievement_by_id(
    achievement_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Achievement).where(Achievement.id == achievement_id)
    )
    achievement = result.scalars().first()

    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Achievement with ID {achievement_id} not found"
        )

    return achievement
    
