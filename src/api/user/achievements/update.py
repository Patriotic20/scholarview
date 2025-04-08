from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from src.models.achievements import Achievement
from src.schemas.achievement import AchievementUpdate
from sqlalchemy.future import select


update_router = APIRouter()


@update_router.put("/update")
async def update(
    item_id : int ,
    update_items: AchievementUpdate,
    db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(Achievement).where(Achievement.id == item_id))
    achievement = result.scalars().first()


    if not achievement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Achievements not fuond"
        )

    for field , value in update_items.model_dump(exclude_unset=True).items():
        if value in ("" , None , "string"):
            continue
        setattr(achievement , field , value)

    await db.commit()
    await db.refresh(achievement)

    return achievement


