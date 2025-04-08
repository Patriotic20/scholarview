from fastapi import APIRouter , Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.base import get_db
from sqlalchemy.future import select
from src.models import ForeignLanguageCertificate

delete_router = APIRouter()


@delete_router.delete("/delete")
async def delete(
    certificate_id: int,
    db: AsyncSession = Depends(get_db)):

    result = await db.execute(select(ForeignLanguageCertificate).where(ForeignLanguageCertificate.id == certificate_id))
    certificate = result.scalars().first()

    await db.delete(certificate)
    await db.commit()

    return {"message": "Delete certificate"}
    