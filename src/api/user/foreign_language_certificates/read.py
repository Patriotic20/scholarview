from fastapi import APIRouter , Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.models import ForeignLanguageCertificate
from src.core.base import get_db
from typing import List
from src.schemas.foreign_language_certificates import ForeignLanguageCertificateResponse

read_router = APIRouter()

@read_router.get("/get-all" , response_model=List[ForeignLanguageCertificateResponse])
async def read(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ForeignLanguageCertificate).limit(10))
    certificate = result.scalars().all()

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )

    return certificate
    

 
@read_router.get("/get/{certificate_id}" , response_model=ForeignLanguageCertificateResponse)
async def read_all(
    certificate_id: int,
    db: AsyncSession = Depends(get_db)):

    result=await db.execute(select(ForeignLanguageCertificate).where(ForeignLanguageCertificate.id == certificate_id))
    certificate = result.scalars().first()

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )

    return certificate


