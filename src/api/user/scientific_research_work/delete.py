from fastapi import APIRouter , Depends , HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from src.core.base import get_db
from src.schemas import DeleteResponse
from src.models.scientific_research_work import ScientificResearchWork   

delete_router = APIRouter()


@delete_router.delete(
    "/{item_id}",
    response_model=DeleteResponse,
    summary="Delete a scientific research work",
    description="Deletes a scientific research work by its ID if it exists",
    responses={
        200: {"description": "Research work deleted successfully"},
        404: {"description": "Research work not found"},
        500: {"description": "Internal server error"}
    }
)
async def delete_research_work(
    item_id: int,
    db: AsyncSession = Depends(get_db)
):
    try:
        
        result = await db.execute(
            select(ScientificResearchWork).where(
                ScientificResearchWork.id == item_id
            )
        )
        research_work = result.scalars().first()

        
        if not research_work:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Research work with ID {item_id} not found"
            )


        await db.delete(research_work)
        await db.commit()

        return DeleteResponse(
            message="Research work deleted successfully",
            deleted_id=item_id
        )

    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting research work: {str(e)}"
        )