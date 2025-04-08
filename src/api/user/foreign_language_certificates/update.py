from fastapi import APIRouter, Depends , HTTPException , status
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from sqlalchemy.future import select
from src.models.foreign_language_certificates import ForeignLanguageCertificate
from src.schemas.foreign_language_certificates import ForeignLanguageCertificateUpdate , ForeignLanguageCertificateResponse

update_router = APIRouter()


@update_router.put("/update" , response_model=ForeignLanguageCertificateResponse)
async def update(
    Certificate_id : int,
    update_item : ForeignLanguageCertificateUpdate,
    db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(ForeignLanguageCertificate).where(ForeignLanguageCertificate.id == Certificate_id))
    certificate = result.scalars().first()

    if not certificate:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Certificate not found"
        )
    
    for field , value in update_item.model_dump(exclude_unset=True).items():
        if value in ("", "string" , None):
            continue
        setattr(certificate , field , value)


    await db.commit()
    await db.refresh(certificate)

    return certificate
