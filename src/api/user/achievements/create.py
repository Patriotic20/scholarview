from fastapi import APIRouter , Depends  , UploadFile , File , HTTPException , status 
from src.core.base import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.achievements import Achievement
from sqlalchemy.exc import SQLAlchemyError
from src.utils.upload_file import save_file

from datetime import date

create_router = APIRouter()


@create_router.post("/create")
async def create(
    name: str ,
    type_of_achievement: str,
    date_of_award_of_achievement : date,
    file: UploadFile = File(...) ,
    db: AsyncSession = Depends(get_db)):
    
    
    file_path = await save_file(file=file)

    new_achievement = Achievement(
        type_of_achievement=type_of_achievement,
        name=name,
        date_of_award_of_achievement=date_of_award_of_achievement,
        file_path=file_path
    )

    try:
        db.add(new_achievement)
        await db.commit()
        await db.refresh(new_achievement)
    except SQLAlchemyError as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {e}"
        )
    
    return new_achievement