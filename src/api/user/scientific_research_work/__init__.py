from fastapi import APIRouter
from .create import create_router
from .update import update_router
from .delete import delete_router
from .read import read_router


scientific_research_work_router  = APIRouter(
    tags=["Scientific research work"],
    prefix="/scientific_research_work"
)


scientific_research_work_router.include_router(create_router)
scientific_research_work_router.include_router(update_router)
scientific_research_work_router.include_router(delete_router)
scientific_research_work_router.include_router(read_router)