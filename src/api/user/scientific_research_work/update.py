from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from sqlalchemy.future import select
from src.schemas.scientific_research_work import ScientificResearchWorkUpdate , ScientificResearchWorkResponse
from src.models.scientific_research_work import ScientificResearchWork

update_router = APIRouter()


@update_router.put("/update" , response_model=ScientificResearchWorkResponse)
async def update(
    item_id: int,
    update_item : ScientificResearchWorkUpdate,
    db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(ScientificResearchWork).where(ScientificResearchWork.id == item_id))
    result = result.scalars().first()

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )
    
    for field , value in update_item.model_dump(exclude_unset=True).items():
        if value in ("" , None , "string"):
            continue
        setattr(result , field , value)

    await db.commit()
    await db.refresh(result)
    return result
    

