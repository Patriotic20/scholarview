from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.base import get_db
from src.models.scientific_research_work import ScientificResearchWork
from src.schemas.scientific_research_work import ScientificResearchWorkResponse

read_router = APIRouter()


@read_router.get("/works", response_model=List[ScientificResearchWorkResponse])
async def get_all_works(db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(ScientificResearchWork))
    works = result.scalars().all()
    return works


@read_router.get("/works/{work_id}", response_model=ScientificResearchWorkResponse)
async def get_work_by_id(work_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(ScientificResearchWork).where(ScientificResearchWork.id == work_id)
    )
    work = result.scalars().first()  

    if not work:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Work not found"
        )
    return work
