from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.core.base import get_db
from src.models.scientific_research_work import ScientificResearchWork
from src.utils.upload_file import save_file

create_router = APIRouter()

@create_router.post("/create")
async def create(
    scientific_research_form: str = Form(...),
    name: str = Form(...),
    date_of_publication: date = Form(...),
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db)
):
    
    file_path = await save_file(file=file)

    
    new_work = ScientificResearchWork(
        scientific_research_form=scientific_research_form,
        date_of_publication=date_of_publication,
        name=name,
        file_path=file_path
    )

    try:
        
        db.add(new_work)
        await db.commit()

        await db.refresh(new_work)
        return {"message": "Scientific research work created successfully.", "work": new_work}
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error: {e}"
        )
