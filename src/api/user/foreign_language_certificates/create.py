from fastapi import APIRouter , Depends  , UploadFile , File , HTTPException , status
from src.core.base import get_db
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from src.models.foreign_language_certificates import ForeignLanguageCertificate
from src.utils.upload_file import save_file



create_router = APIRouter()


@create_router.post("/create")
async def create(
    language : str,
    certificate_type: str,
    level: str,
    series_and_number: str,
    date_of_issue:  date,
    file : UploadFile = File(...),
    db: AsyncSession = Depends(get_db)):

    file_path = await save_file(file)

    
    check_by_series = await db.execute(
        select(ForeignLanguageCertificate).where(ForeignLanguageCertificate.series_and_number == series_and_number)
    )
    check_by_series = check_by_series.scalars().first()

    if check_by_series:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,  
            detail="A certificate with this series and number already exists."
        )

    
    new_certificate = ForeignLanguageCertificate(
        language=language,
        certificate_type=certificate_type,
        level=level,
        series_and_number=series_and_number,
        date_of_issue=date_of_issue,
        file_path=file_path
    )

    try:
        db.add(new_certificate)
        await db.commit()
        await db.refresh(new_certificate)
        return new_certificate  
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while saving the certificate: {str(e)}"
        )